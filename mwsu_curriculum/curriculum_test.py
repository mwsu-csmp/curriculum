import inspect
from .curriculumlib import *
from os import listdir

########################################################################
# Test Syllabi 
########################################################################

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

def test_topic_coverage():
    syl = load_syllabus('2019-2020', 'ACT', '324')
    assert len(syl.topics) == 9
    topic = syl.topics[1]
    assert topic is not None
    assert topic.text.strip() == 'Software Testing Practices'
    subtopic = topic.subtopics[0]
    assert subtopic is not None
    assert subtopic.text.strip() == 'Test driven development'
    assert subtopic.coverages is not None
    assert len(subtopic.coverages) == 1
    coverage = subtopic.coverages[0]
    assert coverage['standard'] == 'acm-cs2013'
    assert coverage['id']== '8'
    assert coverage['knowledgeArea'] == 'SE/SVAV'


#Testing hours_per_semester
def test_hours_per_semester_is_not_none():
    assert hours_per_semester('2019-2020') is not None

def test_hours_per_semester_is_not_an_empty_list():
    assert hours_per_semester('2019-2020') is not []

def test_hours_per_semester_returns_a_list():
    assert isinstance(hours_per_semester('2019-2020'), list)

#Testing courses_in_semester 
def test_courses_in_semester_is_not_none():
    assert courses_in_semester('2019-2020', 'fa') is not None

def test_every_year_courses():
    assert 'CSC184' in courses_in_semester('2019-2020', 'fa')
    assert 'CSC254' in courses_in_semester('2019-2020', 'fa')
    assert 'CSC184' in courses_in_semester('2019-2020', 'sp')
    assert 'CSC254' in courses_in_semester('2019-2020', 'sp')

def test_wrong_semester_courses():
    assert 'CSC406' not in courses_in_semester('2019-2020', 'fa')
    assert 'CSC406' in courses_in_semester('2019-2020', 'sp')

def test_oddg_semester_courses():
    assert 'CSC345' not in courses_in_semester('2019-2020', 'fa')
    assert 'CSC345' not in courses_in_semester('2019-2020', 'sp')
    assert 'CSC345' not in courses_in_semester('2018-2019', 'fa')
    assert 'CSC345' in courses_in_semester('2018-2019', 'sp')

def test_hours_adjusted_in_schedule():
    sp19schedule = load_schedule('sp', '19')
    for course in sp19schedule:
        if course.subject+course.number == 'CSC590':
            section = sp19schedule[course][0]
            assert section.workload_hours == 2


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

def test_section_duration():
  sp19schedule = load_schedule('sp', '19')
  for course in sp19schedule:
      if course.subject+course.number == 'CSC184':
          for section in sp19schedule[course]:
              if section.section == '01':
                  assert section.startTime == '9:30'
                  assert section.duration() == 80

########################################################################
# Test Roster
########################################################################

def test_parse_roster():
  roster = load_roster('2019-2020')
  assert len(roster) > 0
  for instructor in roster:
    assert isinstance(instructor, Instructor)

########################################################################
# Test Standards
########################################################################

def test_parse_standards():
  standards = load_standards()
  assert len(standards) > 0
  for standard in standards:
    assert isinstance(standard, str)
    assert isinstance(standards[standard], Standard)

def test_cs2017_standard_content():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    assert cs2017
    assert cs2017.name == 'Computer Science Curricula'
    assert cs2017.body == 'acm/ieee'
    assert cs2017.version == '2013'
    assert cs2017.kas
    assert cs2017.kas['SE']
    sp = cs2017.kas['SE']
    assert sp.name == 'Software Engineering'
    assert sp.kas['SVAV']
    svav = sp.kas['SVAV']
    assert svav.name == 'Software Verification and Validation'
    assert len(svav.topics) == 17
    assert len(svav.outcomes) == 17
    topic = svav.topics[1]
    assert topic.text.strip() == 'Inspections, reviews, audits'
    assert topic.importance == 'tier2'
    outcome = svav.outcomes[0]
    assert outcome.text.strip() == 'Distinguish between program validation and verification.'
    assert outcome.importance == 'tier2'
    assert outcome.mastery_level == 'familiarity'

def test_outcome_coverage_list():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    syl = load_syllabus('2019-2020', 'ACT', '324')
    assert syl.get_outcome_coverages()

def test_outcome_coverage_lookup():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    syl = load_syllabus('2019-2020', 'ACT', '324')
    outcome = syl.objectives[0]
    coverage = outcome.coverages[0]
    loutcome = cs2017.outcome_coverage_lookup(coverage)
    assert loutcome

def test_topic_coverage_lookup():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    syl = load_syllabus('2019-2020', 'ACT', '324')
    topic = syl.topics[1]
    subtopic = topic.subtopics[0]
    coverage = subtopic.coverages[0]
    ltopic = cs2017.topic_coverage_lookup(coverage)
    assert ltopic

def test_topic_coverage_lookup_direct():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    ka = cs2017.kas['SDF']
    assert ka
    ska = ka.kas['AAD']
    assert ska
    topic = ska.topics[1]
    assert topic
   

def test_every_outcome_coverage():
    standards = load_standards()
    for ay in available_years():
        syllabi = load_syllabi(ay)
        for syllabus in syllabi:
            for outcome in syllabus.objectives:
                for coverage in outcome.coverages:
                    if coverage['standard'] in standards: # todo: change to assertion once all standards are in place
                      standard = standards[coverage['standard']]
                      assert coverage['id'].isdigit(), syllabus.subject + "-" + syllabus.number + " has bad coverage"
                      outcome = standard.outcome_coverage_lookup(coverage)
                      assert outcome, str(coverage) + " not found"


def test_every_topic_coverage():
    standards = load_standards()
    for ay in available_years():
        syllabi = load_syllabi(ay)
        for syllabus in syllabi:
            topics = syllabus.topics
            while topics:
                topic = topics[0]
                topics = topics[1:]
                if topic.subtopics:
                    topics.extend(topic.subtopics)
                for coverage in topic.coverages:
                    if coverage['standard'] in standards: # todo: change to assertion once all standards are in place
                      standard = standards[coverage['standard']]
                      topic = standard.topic_coverage_lookup(coverage)
                      assert topic, str(coverage) + " not found"


def test_add_coverage():
    standards = load_standards()
    cs2013 = standards['acm-cs2013']
    assert cs2013.outcome_coverage() == 0
    assert cs2013.topic_coverage() == 0
    syl = load_syllabus('2019-2020', 'ACT', '324')
    ka = cs2013.kas['SE']
    assert ka.outcome_coverage() == 0.0
    assert ka.topic_coverage() == 0.0

    # add ACT324 syllabus coverages and check coverage level
    cs2013.add_coverage(syl)
    # TODO: update later with specific number once coverages settle
    assert cs2013.outcome_coverage() > 0
    assert cs2013.topic_coverage() > 0
    assert ka.outcome_coverage() > 0
    assert ka.topic_coverage() > 0 


