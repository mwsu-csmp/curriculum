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

#Testing hours_per_semester

def test_hours_per_semester_is_not_none():
    assert hours_per_semester() is not None

def test_hours_per_semester_is_not_an_empty_list():
    assert hours_per_semester() is not []

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

def test_hours_per_semester_():
    assert len(hours_per_semester()[1])

#Testing courses_per_semester

def test_courses_per_semester_is_not_none():
    assert courses_per_semester() is not None

def test_courses_per_semester_returns_a_class():
    assert inspect.isclass(courses_per_semester())

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

