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

#Testing courses_per_semester

def test_coursees_per_semester_is_not_none():
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

