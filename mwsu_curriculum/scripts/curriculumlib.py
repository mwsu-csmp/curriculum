import xml.etree.ElementTree as ET
from os import walk
from collections import defaultdict

class Syllabus:
  title = None
  subject = None
  number = None
  offered = None
  workload_hours = None
  
def parse_syllabus(xmlfile):
  ns = '{https://csmp.missouriwestern.edu}'
  dt = ET.parse(xmlfile).getroot()
  syllabus = Syllabus()
  
  syllabus.title = dt.find(ns+'title').text
  syllabus.subject = dt.find(ns+'subject').text
  syllabus.number = dt.find(ns+'number').text
  syllabus.workload_hours = int(3 if not 'workloadHoursLecture' in dt.attrib else dt.attrib['workloadHoursLecture'])
  syllabus.offered = list()
  for semestert in dt.findall(ns+'offered'):
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
  return [parse_syllabus(open('syllabi/'+filename)) for filename in next(walk('syllabi'))[2]]

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
