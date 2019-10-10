import xml.etree.ElementTree as ET
import os
from os import walk
from collections import defaultdict
from pkg_resources import resource_filename


class Syllabus:
    title = None
    subject = None
    number = None
    offered = None
    workload_hours = 0
    scheduleType = None
    catalogDescription = None
    prerequisites = None
    objective = None
    topic = None


class Schedule:
    course = None
    sectionNumber = None
    StartTime = None
    EndTime = None
    day = None
    buildingRoom = None
    max = None
    instructor = None


def parse_syllabus(xmlfile):
    ns = '{https://csmp.missouriwestern.edu}'
    dt = ET.parse(xmlfile).getroot()
    syllabus = Syllabus()

    syllabus.title = dt.find(ns + 'title').text
    syllabus.subject = dt.find(ns + 'subject').text
    syllabus.number = dt.find(ns + 'number').text
    syllabus.workload_hours = int(3 if not 'workloadHoursLecture' in dt.attrib else dt.attrib['workloadHoursLecture'])
    syllabus.offered = list()
    for semestert in dt.findall(ns + 'offered'):
        semester = semestert.text
        if semester == 'spring':
            syllabus.offered.append('spring-even')
            syllabus.offered.append('spring-odd')
        elif semester == 'fall':
            syllabus.offered.append('fall-even')
            syllabus.offered.append('fall-odd')
        else:
            syllabus.offered.append(semester)

    return syllabus


def load_syllabi():
    syllabi = []
    for filename in next(walk(resource_filename('mwsu_curriculum', 'syllabi')))[2]:
        syllabi.append(parse_syllabus(open(resource_filename('mwsu_curriculum', 'syllabi/' + filename))))
    return syllabi


def parse_course(filename):
    ns = '{https://csmp.missouriwestern.edu}'
    syllabus = Syllabus()
    dt = ET.parse(filename).getroot()
    syllabus.title = dt.find(ns + 'title').text
    syllabus.subject = dt.find(ns + 'subject').text
    syllabus.number = dt.find(ns + 'number').text
    syllabus.workload_hours = int(3 if not 'workloadHoursLecture' in dt.attrib else dt.attrib['workloadHoursLecture'])
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


def load_courses():
    syllabi = []
    for filename in next(walk(resource_filename('mwsu_curriculum', 'syllabi')))[2]:
        syllabi.append(parse_course(open(resource_filename('mwsu_curriculum', 'syllabi/' + filename))))
    return syllabi


def parse_schedule(filename):
    ns = '{https://csmp.missouriwestern.edu}'
    schedule = Schedule()
    dt = ET.parse(filename).getroot()
    schedule.course = list()
    schedule.sectionNumber = list()
    schedule.StartTime = list()
    schedule.EndTime = list()
    schedule.buildingRoom = list()
    schedule.instructor = list()
    schedule.day = list()
    schedule.max = list()
    courseinfolist = list()
    returnlist = list()

    for courses in dt.findall(ns + 'courses'):
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


        print(returnlist)

    return returnlist


def load_schedule():
    schedule = []
    path = 'curriculum/mwsu_curriculum/schedules/'
    for filename in os.listdir(path):
        if not filename.endswith(filename): continue
        fullname = path + filename
        schedule.append(parse_schedule(open(fullname)))
    #for filename in next(walk(resource_filename('mwsu_curriculum', 'schedules')))[2]:
    #  schedule.append(parse_course(open(resource_filename('mwsu_curriculum', 'schedules/' + filename))))
    return schedule


def hours_per_semester():
    # update to use credit hours instead of # of courses
    semesters = defaultdict(list)
    for course in load_syllabi():
        for semester in course.offered:
            semesters[semester].append(course)
    ret = []
    for semester in semesters:
        ret.append((semester, sum(map((lambda course: course.workload_hours), semesters[semester]))))
    return ret


def courses_per_semester():
    # update to use credit hours instead of # of courses
    syllabus = Syllabus
    semesters = []
    for course in load_syllabi():
        return syllabus
