import inspect
from .curriculumlib import *


def test_standard():
    pass

#Testing available_years
def test_available_years_count():
    assert len(available_years()) > 0

def test_available_years_format():
    y = available_years()[0]
    print(y)
    assert len(y) == 9
    assert y[4] == '-'
    assert int(y[0:4]) > 2000 
    assert int(y[5:9]) > int(y[0:4])

#Testing load_syllabi
def test_load_syllabi_is_not_none():
    assert load_syllabi('2019-2020') is not None

def test_load_syllabi_is_not_an_empty_list():
    assert load_syllabi('2019-2020') is not []

def test_load_syllabi_returns_a_list():
    assert isinstance(load_syllabi('2019-2020'), list)


#Testing hours_per_semester
def test_hours_per_semester_is_not_none():
    assert hours_per_semester('2019-2020') is not None

def test_hours_per_semester_is_not_an_empty_list():
    assert hours_per_semester('2019-2020') is not []

def test_hours_per_semester_returns_a_list():
    assert isinstance(hours_per_semester('2019-2020'), list)

#This set of tests asserts that hours_per_semester returns a list of tuples
def test_hours_per_semester_returns_a_list_of_tuples():
    assert isinstance(hours_per_semester('2019-2020')[0], tuple)

def test_hours_per_semester_returns_a_list_of_tuples():
    assert isinstance(hours_per_semester('2019-2020')[1], tuple)

def test_hours_per_semester_returns_a_list_of_tuples():
    assert isinstance(hours_per_semester('2019-2020')[2], tuple)

def test_hours_per_semester_returns_a_list_of_tuples():
    assert isinstance(hours_per_semester('2019-2020')[3], tuple)

def test_hours_per_semester_returns_a_list_of_tuples():
    assert isinstance(hours_per_semester('2019-2020')[4], tuple)

def test_hours_per_semester_returns_a_list_of_tuples():
    assert isinstance(hours_per_semester('2019-2020')[5], tuple)

# This set of tests asserts that hours_per_semester returns a list with tuples containing 'spring-even',
# 'spring-odd', 'fall-even', 'fall-odd', 'discretion', and 'summer'
def test_hours_per_semester_contains_spring_even():
    assert any('spring-even' in t for t in hours_per_semester('2019-2020'))

def test_hours_per_semester_contains_spring_odd():
    assert any('spring-odd' in t for t in hours_per_semester('2019-2020'))

def test_hours_per_semester_contains_fall_even():
    assert any('fall-even' in t for t in hours_per_semester('2019-2020'))

def test_hours_per_semester_contains_fall_odd():
    assert any('fall-odd' in t for t in hours_per_semester('2019-2020'))

def test_hours_per_semester_contains_discretion():
    assert any('discretion' in t for t in hours_per_semester('2019-2020'))

def test_hours_per_semester_contains_summer():
    assert any('summer' in t for t in hours_per_semester('2019-2020'))

#This set of tests asserts that hours_per_semester returns a list with tuples with length 2
def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester('2019-2020')[0]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester('2019-2020')[1]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester('2019-2020')[2]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester('2019-2020')[3]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester('2019-2020')[4]) == 2

def test_hours_per_semester_returns_tuples_length_2():
    assert len(hours_per_semester('2019-2020')[5]) == 2

#This set of tests checks that the second element in each tuple returned is an int
def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester('2019-2020')[0][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester('2019-2020')[1][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester('2019-2020')[2][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester('2019-2020')[3][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester('2019-2020')[4][1], int)

def test_hours_per_semester_returns_tuples_with_int():
    assert isinstance(hours_per_semester('2019-2020')[5][1], int)

# This set of tests asserts that the first item in the tuple produced by hours_per_semester is a string
def test_hours_per_semester_returns_tuples_with_string():
    assert isinstance(hours_per_semester('2019-2020')[0][0], str)

def test_hours_per_semester_returns_tuples_with_string():
    assert isinstance(hours_per_semester('2019-2020')[1][0], str)

def test_hours_per_semester_returns_tuples_with_string():
    assert isinstance(hours_per_semester('2019-2020')[2][0], str)

def test_hours_per_semester_returns_tuples_with_string():
    assert isinstance(hours_per_semester('2019-2020')[3][0], str)

def test_hours_per_semester_returns_tuples_with_string():
    assert isinstance(hours_per_semester('2019-2020')[4][0], str)

def test_hours_per_semester_returns_tuples_with_string():
    assert isinstance(hours_per_semester('2019-2020')[5][0], str)


########################################################################
# Test Schedules
########################################################################

def test_parse_schedule():
  sp19schedule = load_schedule('sp', '19')
  assert len(sp19schedule) > 0
  for course in sp19schedule:
    assert isinstance(course, Syllabus)
    assert len(sp19schedule[course]) > 0
    for section in sp19schedule[course]:
      assert isinstance(section, Section)



########################################################################
# Test Schedules
########################################################################

def test_parse_roster():
  roster = load_roster('2019-2020')
  assert len(roster) > 0
  for instructor in roster:
    assert isinstance(instructor, Instructor)


