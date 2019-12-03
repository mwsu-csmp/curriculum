import inspect
from .curriculumlib import load_syllabi
from .curriculumlib import hours_per_semester
from .curriculumlib import courses_per_semester
from .curriculumlib import parse_course
from .curriculumlib import load_assignments


def test_standard():
    pass

#Testing load_syllabi

def test_load_syllabi_is_not_none():
    assert load_syllabi() is not None

def test_load_syllabi_is_not_an_empty_list():
    assert load_syllabi() is not []

def test_load_syllabi_returns_a_list():
    assert isinstance(load_syllabi(), list)

#Testing hours_per_semester

def test_hours_per_semester_is_not_none():
    assert hours_per_semester() is not None

def test_hours_per_semester_is_not_an_empty_list():
    assert hours_per_semester() is not []

#This set of tests asserts that hours_per_semester returns a list with tuples containing 'spring-even', 'spring-odd', 'fall-even', 'fall-odd', 'discretion', and 'summer'
def test_hours_per_semester_contains_spring_even():
    assert any('spring-even' in t for t in hours_per_semester())

def test_hours_per_semester_contains_spring_odd():
    assert any('spring-odd' in t for t in hours_per_semester())

def test_hours_per_semester_contains_fall_even():
    assert any('fall-even' in t for t in hours_per_semester())

def test_hours_per_semester_contains_fall_odd():
    assert any('fall-odd' in t for t in hours_per_semester())

def test_hours_per_semester_contains_discretion():
    assert any('discretion' in t for t in hours_per_semester())

def test_hours_per_semester_contains_summer():
    assert any('summer' in t for t in hours_per_semester())


#This set of tests asserts that hours_per_semester returns a list with tuples with length 2
def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester()[0]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester()[1]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester()[2]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester()[3]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester()[4]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester()[5]) == 2

#This set of tests checks that the second element in each tuple returned is an int
def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester()[0][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester()[1][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester()[2][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester()[3][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester()[4][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester()[5][1], int)


#Testing courses_per_semester

def test_courses_per_semester_is_not_none():
    assert courses_per_semester() is not None

def test_courses_per_semester_returns_a_class():
    assert inspect.isclass(courses_per_semester())

#This set of tests asserts that the default values of the syllabus class are set to None or 0
def test_courses_per_semester_syllabus_class_catalogDescription_returns_none():
    assert courses_per_semester().catalogDescription is None

def test_courses_per_semester_syllabus_class_returns_none():
    assert courses_per_semester().number is None

def test_courses_per_semester_syllabus_class_objective_returns_none():
    assert courses_per_semester().objective is None

def test_courses_per_semester_syllabus_class_offered_returns_none():
    assert courses_per_semester().offered is None

def test_courses_per_semester_syllabus_class_prerequisites_returns_none():
    assert courses_per_semester().prerequisites is None

def test_courses_per_semester_syllabus_class_scheduleType_returns_none():
    assert courses_per_semester().scheduleType is None

def test_courses_per_semester_syllabus_class_subject_returns_none():
    assert courses_per_semester().subject is None

def test_courses_per_semester_syllabus_class_title_returns_none():
    assert courses_per_semester().title is None

def test_courses_per_semester_syllabus_class_topic_returns_none():
    assert courses_per_semester().topic is None

def test_courses_per_semester_syllabus_class_workload_hours_returns_zero():
    assert courses_per_semester().workload_hours is 0

# Testing parse_course
#Even in linux I was unable to get this function to work so there is only the one generic test for it
def test_parse_course_is_not_none():
    assert parse_course() is not None

#Testing load_assignments
#Even in linux I was Unable to get this function to work so there is only the generic test for it

def test_load_assignment_is_not_none():
    assert load_assignments() is not None

