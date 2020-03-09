import xml.etree.ElementTree as ET
import os
from os import listdir 
from os import walk
from collections import defaultdict
from pkg_resources import resource_filename
from collections import defaultdict

class Topic:
    def __init__(self, dt):
      ns = '{https://csmp.missouriwestern.edu}'
      self.text = dt.text
      self.importance = dt.attrib['importance'] if 'importance' in dt.attrib else None
      
      self.subtopics = list()
      for topict in dt.findall(ns + 'topic'):
        self.subtopics.append(Topic(topict))

class Outcome:
    def __init__(self, dt):
      ns = '{https://csmp.missouriwestern.edu}'
      self.text = dt.text
      self.importance = dt.attrib['importance'] if 'importance' in dt.attrib else None
      self.mastery_level = dt.attrib['mastery_level'] if 'mastery_level' in dt.attrib else None

class KnowledgeArea:
    def __init__(self, dt):
      ns = '{https://csmp.missouriwestern.edu}'
      self.id = dt.attrib['id']
      self.name = dt.attrib['name']
      self.kas = {}
      for kat in dt.findall(ns + 'knowledgeArea'):
        ka = KnowledgeArea(kat)
        self.kas[ka.id] = ka

      self.topics = list()
      for topict in dt.findall(ns + 'topic'):
        self.topics.append(Topic(topict))

      self.outcomes = list()
      for outcomet in dt.findall(ns + 'outcome'):
        self.outcomes.append(Outcome(outcomet))

class Standard:
    """Represents an external standard for curriculum content and objectives"""
    def __init__(self, xmlfile):
      ns = '{https://csmp.missouriwestern.edu}'
      dt = ET.parse(xmlfile).getroot()
      self.name = dt.find(ns + 'name').text
      self.body = dt.find(ns + 'body').text
      self.version = dt.find(ns + 'version').text
      self.url = dt.find(ns + 'documentUrl').text
      self.kas = {}
      for kat in dt.findall(ns + 'knowledgeArea'):
        ka = KnowledgeArea(kat)
        self.kas[ka.id] = ka

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
      self.scheduleType = dt.find(ns + 'scheduleType').text
      self.catalogDescription = dt.find(ns + 'catalogDescription').text
      self.prerequisites = dt.find(ns + 'prerequisites').text
      self.objective = list()
      for objectivet in dt.findall(ns + 'objectives'):
        objective = objectivet.find(ns + 'objective').text
        self.objective.append(objective)
      self.topic = list()
      for topict in dt.findall(ns + 'outline'):
        topic = topict.find(ns + 'topic').text
        self.topic.append(topic)

class Section:
    def __init__(self,course,section,instructorId,maxEnrollment,startTime=None,endTime=None,days=[],building=None,room=None):
        self.course = course
        self.section = section
        self.instructorId = instructorId
        self.maxEnrollment = maxEnrollment
        self.startTime = startTime
        self.endTime = endTime
        self.days = days
        self.building = building
        self.room = room

    def duration(self):
        if not self.startTime or not self.endTime:
            return 0
        h1, m1 = map(int, self.startTime.split(':'))
        h2, m2 = map(int, self.endTime.split(':'))
        if h1 < 8:
            h1 += 12
            h2 += 12
        elif h2 < h1:
            h2 += 12
        return (60*(h2 - h1) + (m2 - m1))

    def conflicts_with(self, otherSection):
        if not self.startTime or \
                not self.endTime or \
                not otherSection.startTime or \
                not otherSection.endTime:
            return False # at least one course does not meet at a scheduled time

        if not (set(self.days) & set(otherSection.days)):
            return False # no intersecting days

        h1, m1 = map(int, self.startTime.split(':'))
        h2, m2 = map(int, self.endTime.split(':'))
        if h1 < 8:
            h1 += 12
            h2 += 12
        elif h2 < h1:
            h2 += 12
        m1 += h1*60
        m2 += h2*60
        oh1, om1 = map(int, otherSection.startTime.split(':'))
        oh2, om2 = map(int, otherSection.endTime.split(':'))
        if oh1 < 8:
            oh1 += 12
            oh2 += 12
        elif oh2 < oh1:
            oh2 += 12
        om1 += oh1*60
        om2 += oh2*60
        
        return (m1 >= om1 and m1 < om2) or (om1 >= m1 and om1 < m2)

class Instructor:
    def __init__(self, instructorId, name, releases={}):
        self.id = instructorId
        self.name = name
        self.releases = releases

def load_standard(name):
    return Standard(ay, resource_filename('mwsu_curriculum', 'standards/'+name+'.xml'))

def load_standards():
    standards = []
    for filename in next(walk(resource_filename('mwsu_curriculum', 'standards/')))[2]:
        standards.append(Standard(open(resource_filename('mwsu_curriculum', 'standards/' + filename))))
    return {standard.name+'-'+standard.body+'-'+standard.version : standard for standard in standards}

def load_syllabus(ay, subject, number):
    """ loads the specified course (if it exists)"""
    return Syllabus(ay, resource_filename('mwsu_curriculum', 'syllabi/'+ay+'/'+subject+number+'.xml'))

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

def load_roster(ay):
    filename = resource_filename('mwsu_curriculum', 'rosters/'+ay+'.xml')
    ns = '{https://csmp.missouriwestern.edu}'
    dt = ET.parse(filename).getroot()
    roster = []
    for instructort in dt.findall(ns + 'instructor'):
        instructorId = instructort.find(ns + 'id').text
        name = instructort.find(ns + 'name').text
        releases = {}
        for sectiont in instructort.findall(ns + 'release'):
            description = sectiont.find(ns + 'description').text
            hours = int(sectiont.find(ns + 'hours').text)
            releases[description] = hours
        instructor = Instructor(instructorId, name, releases)
        roster.append(instructor)
    return roster

def load_schedule(semester, year):
    if semester == 'fa':
        ay = '20'+year+'-20'+str(int(year)+1)
    else:
        ay = '20'+str(int(year)-1)+'-20'+year
    filename = resource_filename('mwsu_curriculum', 'schedules/'+semester+year+'.xml')
    ns = '{https://csmp.missouriwestern.edu}'
    dt = ET.parse(filename).getroot()
    courses = defaultdict(list)
    for courset in dt.findall(ns + 'course'):
        count = 0
        subject = courset.find(ns + 'subject').text
        number = courset.find(ns + 'number').text
        course = load_syllabus(ay, subject, number)

        for sectiont in courset.findall(ns + 'section'):
            sectionNumber = sectiont.find(ns + 'sectionNumber').text
            instructorId = sectiont.find(ns + 'instructor').text
            maxEnrollment = sectiont.find(ns + 'max').text
            startTime = sectiont.find(ns + 'startTime')
            startTime = startTime.text if startTime is not None else None
            endTime = sectiont.find(ns + 'endTime')
            endTime = endTime.text if endTime is not None else None
            building = sectiont.find(ns + 'building')
            building = building.text if building is not None else None
            room = sectiont.find(ns + 'room')
            room = room.text if room is not None else None
            daysList = list()
            for days in sectiont.findall(ns + 'day'):
                day = days.text
                daysList.append(day)
            section = Section(course,sectionNumber,instructorId,maxEnrollment,days=daysList,
                    startTime=startTime, endTime=endTime, building=building, room=room)
            courses[course].append(section)
    return courses

def available_years():
    """ returns a list of academic-year (20XX-20YY) strings for all available years of curriculum definitions"""
    return list(listdir(resource_filename('mwsu_curriculum', 'syllabi/')))

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
