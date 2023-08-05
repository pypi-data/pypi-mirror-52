from collections import namedtuple, OrderedDict, MutableMapping
import itertools
import logging
import lxml.html
import requests


logger = logging.getLogger(__name__)


class Schedule:
    Term = namedtuple('Term', ['code', 'name'])
    Course = namedtuple('Course', ('department_code', 'number', 'title', 'units'))
    Section = namedtuple('Section', [
        'CRN',
        'department_code',
        'course_number',
        'number',
        'title',
        'notes',
        'activity',
        'days',
        'start_time',
        'end_time',
        'location',
        'instructor',
        'max_seats',
        'taken_seats',
        'free_seats'
    ])

    def __init__(self, schedule_html, term):
        self.html = schedule_html
        self.term = term
        self.departments, self.courses, self.sections = _parse_tables(self.html)
    
    @classmethod
    def fetch(cls, term):
        return cls(_fetch_schedule_page(term.code), term)

    @classmethod
    def fetch_latest(cls):
        return cls.fetch(get_current_terms()[-1])


def get_current_terms():
    if get_current_terms.terms is None:
        get_current_terms.terms = _fetch_terms()
    return get_current_terms.terms
get_current_terms.terms = None


def _fetch_terms():
    course_search_page = requests.get(
        'https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.p_selectsubject'
    ).content
    document = lxml.html.fromstring(course_search_page)

    """
    In the schedule search form, each term line is a <tr>, e.g.:
    <tr>
        <td class="pldefault">
            <input type="radio" name="validterm" value="201930" checked="">
        </td>
        <td class="pldefault">Fall Semester 2019</td>
    </tr>
    """
    def code(button):
        return button.get('value')

    return tuple([
        Schedule.Term(code(button), button.getparent().getnext().text_content())
        for button in document.cssselect('input[name="validterm"]')
    ])


def _fetch_schedule_page(code):
    return requests.post(
        'https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_ViewSchedule',
        data={
            'validterm': code,
            'subjcode': 'ALL',
            'openclasses': 'N'
        }
    ).text


def _parse_departments(tables):
    def get_department_code(table):
        FIRST_COURSE_ROW = 1
        DEPARTMENT_ID_COLUMN = 1
        department_id_cell = table[FIRST_COURSE_ROW][DEPARTMENT_ID_COLUMN]
        # Example text_content(): 'ANTH-001-01'
        return department_id_cell.text_content().split('-')[0]

    def get_department_name(table):
        # Department class table is always immediately preceded by a h3 with the
        # department's full name
        return table.getprevious().text_content()

    return OrderedDict([
        (get_department_code(table), get_department_name(table))
        for table in tables
    ])


def _parse_tables(schedule_page):
    document = lxml.html.fromstring(schedule_page)
    tables = document.cssselect('table.datadisplaytable')

    departments = _parse_departments(tables)

    def is_class_row(row): # as opposed to an EXAM row
        # Course title cells ALWAYS have the 'rowspan' attribute
        TITLE_COLUMN = 2
        return row[TITLE_COLUMN].get('rowspan')

    all_rows = (row for table in tables for row in table)
    class_rows = filter(is_class_row, all_rows)

    # Convert rows to section dicts
    sections = []
    for r in class_rows:
        try:
            s = _row_to_section(r)
        except Exception:
            logger.exception('Could not parse:\n%s', lxml.html.tostring(r))
        else:
            sections.append(s)

    # Extract courses before sections are purged of Course-only fields
    courses = _extract_courses(sections)

    for s in sections:
        # keep only department_code, course_number, and title (foreign keys on Courses)
        del s['units']
    def sectionify(s):
        return Schedule.Section(*[s[f] for f in Schedule.Section._fields])

    return departments, courses, tuple([sectionify(s) for s in sections])


def _extract_courses(sections):
    def coursify(section):
        # convert 'course_number' to 'number'
        fields = Schedule.Course._fields
        values = [section[f] for f in fields if f != 'number']
        values.insert(fields.index('number'), section['course_number'])
        return Schedule.Course(*values)

    # use OrderedDict instead of set to guarantee order and, by  exploiting the
    # uniqueness of keys in dicts, to guarantee course uniqueness
    courses_as_keys = OrderedDict([
        (coursify(s), None) # courses stored as keys for aforementioned behavior; associated value does not matter
        for s in sections
        # Do not make courses out of unitless sections (which would otherwise
        # get their own course in this set because the 0-units would make a
        # unique identity) UNLESS the unitless section is a main (i.e.
        # not supplementary like DISC or LAB) section
        if s['units'] > 0 or s['activity'] in ('LECT', 'SEM')
    ])

    return tuple(courses_as_keys.keys())


def _row_to_section(row):
    def get_text(cell):
        return cell.text_content()

    def get_number(cell):
        try:
            return int(cell.text_content())
        except ValueError:
            return 0

    def reject(cell):
        return None

    def fieldify_department_id(cell):
        subfields = cell.text_content().split('-')
        return OrderedDict([
            ('department_code', subfields[0]),
            ('course_number', subfields[1]),
            ('number', subfields[2])
        ])

    def fieldify_title(cell):
        text_lines = [s.title() for s in cell.itertext()] # note the normalization via s.title()

        # There are multi-line title cells with a rowspan of 1, unfortunately
        # That includes the case where the other line is a "Must Also Register"
        # AND includes the case where the other line is like, a subtitle, e.g.
        # "Journal Club\nCardiovascular Tissue Engineering"
        # if cell.get('rowspan') == '1' or len(textLines) == '1':
        #     return '\n'.join(textLines)
        # So the following is the safest:
        if len(text_lines) == 1:
            return {
                'title': text_lines[0],
                'notes': ''
            }
        else:
            result = {
                'title': text_lines[0],
                'notes': ''
            }

            # Distinguish sub-titles from note info
            notes_started = False
            for note_beginning, line in enumerate(text_lines[1:]): # skip title line 0
                for note_indicator in ('Must ', 'Class ', 'Includes '):
                    if note_indicator in line:
                        notes_started = True
                        break
                if notes_started: break
            if notes_started:
                for j in range(1, 1 + note_beginning): # sync with text_lines[1:]
                    result['title'] += '\n' + text_lines[j]
                for j in range(1 + note_beginning, len(text_lines)):
                    result['notes'] += '\n' + text_lines[j]
                result['notes'] = result['notes'].lstrip()
            else:
                result['title'] = '\n'.join(text_lines)

            return result


    def fieldify_time(cell):
        time_text = cell.text_content()
        if 'TBD' in time_text:
            return OrderedDict([('start_time', 'TBD'), ('end_time', 'TBD')])

        def to_minutes(time_string):
            hours, minutes = time_string.split(':')
            return int(hours) * 60 + int(minutes)

        raw_start, raw_end = time_text.split('-')
        start = to_minutes(raw_start)
        end = to_minutes(raw_end[:-2])
        if raw_end[-2:] == "pm" and not (to_minutes('12:00') <= end <= to_minutes('12:59')):
            if start < end:
                start += 12 * 60
            end += 12 * 60

        def to_time_string(time):
            return '{}:{} {}'.format(
                str(time // 60 % 12 or 12), # circuit to 12 if % 12 == 0
                str(time % 60 or '00'), # circuit to '00' if % 60 == 0
                ('PM' if time >= to_minutes('12:00') else 'AM')
            )

        return OrderedDict([('start_time', to_time_string(start)), ('end_time', to_time_string(end))])

    COLUMN_TRANSFORMS = (
        ('CRN', get_number),
        ('department_id', fieldify_department_id),
        ('title', fieldify_title),
        ('units', get_number),
        ('activity', get_text),
        ('days', get_text),
        ('time', fieldify_time),
        ('location', get_text),
        ('term_length', reject),
        ('instructor', get_text),
        ('max_seats', get_number),
        ('taken_seats', get_number),
        ('free_seats', get_number)
    )

    def transpose(pairs):
        # Per https://stackoverflow.com/a/12974504
        return zip(*pairs)

    section = OrderedDict([
        (key, transform(cell))

        for cell, key, transform
        in zip(row, *transpose(COLUMN_TRANSFORMS))
        if transform is not reject
    ])

    # make new dict with dict-value fields merged in
    flat_section = OrderedDict()
    for k, v in section.items():
        if isinstance(v, MutableMapping):
            for k_in, v_in in v.items():
                flat_section[k_in] = v_in
        else:
            flat_section[k] = v

    return flat_section
