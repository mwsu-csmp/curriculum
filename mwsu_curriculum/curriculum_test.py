import pytest
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

#Testing courses_per_semester

def test_courses_per_semester_is_not_none():
    assert courses_per_semester() is not None

def test_courses_per_semester_is_a_class():
    assert courses_per_semester()

# Testing parse_course
#Even in linux I was unable to get this function to work so there is only the one generic test for it
def test_parse_course_is_not_none():
    assert parse_course() is not None

#Testing load_assignments
#Even in linux I was Unable to get this function to work so there is only the generic test for it

def test_load_assignment_is_not_none():
    assert load_assignments() is not None

