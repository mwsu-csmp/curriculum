import xml.etree.ElementTree as ET
import os
from os import listdir 
from os import walk
from collections import defaultdict
from pkg_resources import resource_filename


class Syllabus:
    """ Creates a class for each syllabi. These consist of a title, subject, course number, when it is offered
      the workload hours, the schedule type, the course description, course prerequisites, course objectices,
      and course topics"""
    def __init__(self, ay, xmlfile):
      """ parses the XML file and collects the information which includes title, subject, number, workload hours,
       offered, and what semester offered """
      ns = '{https://csmp.missouriwestern.edu}'
      dt = ET.parse(xmlfile).getroot()
      self.title = dt.find(ns + 'title').text
      self.ay = ay
      self.subject = dt.find(ns + 'subject').text
      self.number = dt.find(ns + 'number').text
      self.workload_hours = int(3 if not 'workloadHoursLecture' in dt.attrib else dt.attrib['workloadHoursLecture'])
      self.offered = list()
      for semestert in dt.findall(ns + 'offered'):
        semester = semestert.text
        if semester == 'spring':
            self.offered.append('spring-even')
            self.offered.append('spring-odd')
        elif semester == 'fall':
            self.offered.append('fall-even')
            self.offered.append('fall-odd')
        else:
            self.offered.append(semester)
    title = None
    subject = None
    number = None
    ay = None
    offered = None
    workload_hours = 0
    scheduleType = None
    catalogDescription = None
    prerequisites = None
    objective = None
    topic = None

def available_years():
    """ returns a list of academic-year (20XX-20YY) strings for all available years of curriculum definitions"""
    return list(listdir(resource_filename('mwsu_curriculum', 'syllabi/')))


def load_syllabi(ay):
    """ returns a list containing syllabi for every course defined in the specified academic year's curriculum
    Args:
        ay: academic year (20XX-20YY where YY=XX+1)
    """
    syllabi = []
    for filename in next(walk(resource_filename('mwsu_curriculum', 'syllabi/'+ay)))[2]:
        syllabi.append(Syllabus(ay, \
                open(resource_filename('mwsu_curriculum', 'syllabi/' + ay + '/' + filename))))
    return syllabi

def parse_course(filename):
    """ parses the XML file and collects the information which includes title, subject, number, workload hours,
     offered, and what semester offered, schedule Type, course description, course prerequisites, course objectives,
     and all course topics"""
    ns = '{https://csmp.missouriwestern.edu}'
    syllabus = Syllabus()
    dt = ET.parse(filename).getroot()
    syllabus.title = dt.find(ns + 'title').text
    syllabus.subject = dt.find(ns + 'subject').text
    syllabus.number = dt.find(ns + 'number').text
    syllabus.workload_hours = \
            int(3 if not 'workloadHoursLecture' in dt.attrib else dt.attrib['workloadHoursLecture'])
    syllabus.offered = list()
    for semestert in dt.findall(ns + 'offered'):
        semester = semestert.text
        syllabus.offered.append(semester)
    syllabus.scheduleType = dt.find(ns + 'scheduleType').text
    syllabus.catalogDescription = dt.find(ns + 'catalogDescription').text
    syllabus.prerequisites = dt.find(ns + 'prerequisites').text
    syllabus.objective = list()
    for objectivet in dt.findall(ns + 'objectives'):
        objective = objectivet.find(ns + 'objective').text
        syllabus.objective.append(objective)
    syllabus.topic = list()
    for topict in dt.findall(ns + 'outline'):
        topic = topict.find(ns + 'topic').text
        syllabus.topic.append(topic)

    return syllabus


def load_courses(year):
    """ Goes through and calls parse_syllabus for each XML file inside of the syllabi folder, and puts then in a list """
    syllabi = []
    for filename in next(walk(resource_filename('mwsu_curriculum', 'syllabi')))[2]:
        syllabi.append(parse_course(open(resource_filename('mwsu_curriculum', 'syllabi/' + filename))))
    return syllabi


def parse_schedule(filename):
    """ Goes though and parses each schedule XML file for the courses, course subject and number. course section,
     start time, end time, building room, room capacity, instructor, and days offered """
    ay = str(year) + '-' + str(year+1)   # AY is something like 2020-2021
    ns = '{https://csmp.missouriwestern.edu}'
    dt = ET.parse(filename).getroot()
    courseinfolist = list()
    returnlist = list()

    for courses in dt.findall(ns + 'courses/'+ay):
        for courset in courses.findall(ns + 'course'):
            count = 0
            subject = courset.find(ns + 'subject').text
            number = courset.find(ns + 'number').text
            course = subject + number
            courseinfolist.append(course)
            for sectiont in courset.findall(ns + 'section'):
                count += 1
                if count >= 2:
                    courseinfolist.append(course)

                sectionNumber = sectiont.find(ns + 'sectionNumber').text
                StartTime = sectiont.find(ns + 'StartTime').text
                EndTime = sectiont.find(ns + 'EndTime').text
                buildingRoom = sectiont.find(ns + 'buildingRoom').text
                max = sectiont.find(ns + 'max').text
                instructor = sectiont.find(ns + 'instructor').text

                courseinfolist.append(sectionNumber)
                courseinfolist.append(StartTime)
                courseinfolist.append(EndTime)
                courseinfolist.append(buildingRoom)
                courseinfolist.append(max)
                courseinfolist.append(instructor)
                dayslist = list()
                for days in sectiont.findall(ns + 'day'):
                    day = days.text
                    dayslist.append(day)
                courseinfolist.append(dayslist)
                a = courseinfolist
                returnlist.append(a)
                courseinfolist = list()


    return returnlist

def parse_assignments(filename):
    """ Parses Assignment XML file, which gets information that includes the instructor, instructor workload, and
     any additional assignments """
    ns = '{https://csmp.missouriwestern.edu}'
    dt = ET.parse(filename).getroot()
    returnlist = list()
    for assignments in dt.findall(ns + 'assignment'):
        assignment_instructor = assignments.find(ns + 'instructor').text
        assignment_credits = assignments.find(ns + 'workhours').text
        returnlist.append(assignment_instructor)
        returnlist.append(assignment_credits)
        print(assignment_instructor)
    return returnlist

def load_assignments():
    """ runs parse_assignments for each XML file in Assignments folder """
    schedule = []
    path = resource_filename('mwsu_curriculum', 'schedules')
    for filename in os.listdir(path):
        fullname = path + '/' + filename
        schedule.append(parse_assignments(open(fullname)))
    return schedule

def load_schedule():
    """ runs parse_schedule for each XML file in Schedule folder """
    schedule = []
    path = resource_filename('mwsu_curriculum', 'schedules')
    for filename in os.listdir(path):
        fullname = path + '/' + filename
        schedule.append(parse_schedule(open(fullname)))
    return schedule


def hours_per_semester(ay):
    """ goes through all the courses and adds up the hours per semester """
    # update to use credit hours instead of # of courses
    semesters = defaultdict(list)
    for course in load_syllabi(ay):
        for semester in course.offered:
            semesters[semester].append(course)
    ret = []
    for semester in semesters:
        ret.append((semester, sum(map((lambda course: course.workload_hours), semesters[semester]))))
    return ret


def courses_per_semester(ay):
    """ goes through the syllabi and collects all of the courses in each semester """
    # update to use credit hours instead of # of courses
    syllabus = Syllabus
    semesters = []
    for course in load_syllabi(ay):
        return syllabus
