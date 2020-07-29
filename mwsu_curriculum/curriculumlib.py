import xml.etree.ElementTree as ET
import os
from os import listdir 
from os import walk
from os import path
from collections import defaultdict
from pkg_resources import resource_filename
from collections import defaultdict

ns = '{https://csmp.missouriwestern.edu}'

class Topic:
    def __init__(self, dt, id, parentid='', standardid=''):
      self.text = dt.text
      self.id = id
      self.covered_by = set()
      self.parentid = parentid
      self.standardid = standardid
      self.importance = dt.attrib['importance'] if 'importance' in dt.attrib else None

      self.coverages = []
      for coverage in dt.findall(ns + 'covers'):
        self.coverages.append(coverage.attrib)

      self.subtopics = list()
      for topict in dt.findall(ns + 'topic'):
        self.subtopics.append(Topic(topict, id + '/' + str(len(self.subtopics)+1), parentid, standardid))

    def add_coverage(self, syllabus):
        """record if the given syllabus covers this topic"""
        for subtopic in self.subtopics:
            subtopic.add_coverage(syllabus)

        coverages = syllabus.get_topic_coverages()
        for oid in coverages:
            for coverage in coverages[oid]:
                # todo: wrong filename (.xml) and ka name not being checked
                if self.standardid == coverage['standard'] and \
                        str(self.id) == coverage['id'] and \
                        self.parentid == coverage['knowledgeArea']:
                    self.covered_by.add((syllabus.subject, syllabus.number, oid))

    def coverage(self):
        """determines the extent to which this topic is covered by recoreded syllabi"""
        if self.covered_by: # covered by something
            return 1
        if not self.subtopics: # not covered by anything and no subtopics for partial coverage
            return 0
        # determine proportion of covered subtopics
        total = 0
        for subtopic in self.subtopics:
            total += subtopic.coverage()
        return total / len(self.subtopics)


class Outcome:
    def __init__(self, dt, id, parentid='', standardid=''):
      self.text = dt.text
      self.id = id
      self.parentid = parentid
      self.standardid = standardid
      self.covered_by = set()
      self.importance = dt.attrib['importance'] if 'importance' in dt.attrib else None
      self.mastery_level = dt.attrib['mastery_level'] if 'mastery_level' in dt.attrib else None

      self.coverages = []
      for coverage in dt.findall(ns + 'covers'):
        self.coverages.append(coverage.attrib)

    def add_coverage(self, syllabus):
        """record if the given syllabus covers this outcome """
        coverages = syllabus.get_outcome_coverages()
        for oid in coverages:
            for coverage in coverages[oid]:
                # todo: wrong filename (.xml) and ka name not being checked
                if self.standardid == coverage['standard'] and \
                        str(self.id) == coverage['id'] and \
                        self.parentid == coverage['knowledgeArea']:
                    self.covered_by.add((syllabus.subject, syllabus.number, oid))

class KnowledgeArea:
    def __init__(self, dt, parentid = None, standardid=None):
      self.id = dt.attrib['id']
      self.standardid = standardid
      self.fullid = parentid + '/' + self.id if parentid else self.id
      self.name = dt.attrib['name'] if 'name' in dt.attrib else ''
      self.kas = {}
      for kat in dt.findall(ns + 'knowledgeArea'):
        ka = KnowledgeArea(kat, self.id, standardid)
        self.kas[ka.id] = ka

      self.topics = list()
      for topict in dt.findall(ns + 'topic'):
        self.topics.append(Topic(topict, str(len(self.topics)+1), self.fullid, standardid))

      self.outcomes = list()
      for outcomet in dt.findall(ns + 'outcome'):
        self.outcomes.append(Outcome(outcomet, len(self.outcomes)+1, self.fullid, standardid))

    def outcome_lookup(self, kas, oid):
        """find topic in this ka"""
        if kas:
          if not self.kas or kas[0] not in self.kas:
            return None
          return self.kas[kas[0]].outcome_lookup(kas[1:], oid)
        if oid <= len(self.outcomes):
          return self.outcomes[oid-1]

    def topic_lookup(self, kas = (), topics = ()):
        """find topic in this ka"""
        if kas:
          if not self.kas or kas[0] not in self.kas:
            return None
          return self.kas[kas[0]].topic_lookup(kas[1:], topics)
        topic = None
        search_topics = self.topics
        while topics:
          id = int(topics[0])
          if not search_topics or id > len(search_topics):
            return None
          topic = search_topics[int(topics[0])-1]
          search_topics = topic.subtopics
          topics = topics[1:]
        return topic

    def add_coverage(self, syllabus):
        """ record what outcomes are covered by the given syllabus """
        for ka in self.kas:
            self.kas[ka].add_coverage(syllabus)
        for outcome in self.outcomes:
            outcome.add_coverage(syllabus)
        for topic in self.topics:
            topic.add_coverage(syllabus)

    def outcome_coverage(self):
        """ determine the coverage level of this ka's outcomes from previously observed syllabi"""
        kas = 0
        total = 0
        for ka in self.kas:
            total += self.kas[ka].outcome_coverage()
            kas += 1

        covered = 0
        for outcome in self.outcomes:
            if outcome.covered_by:
                covered += 1
        if self.outcomes:
            total += covered / len(self.outcomes)
            kas += 1
        if kas:
            return total / kas

        return 1

    def topic_coverage(self):
        """ determine the coverage level of this ka's topics from previously observed syllabi"""
        kas = 0
        total = 0
        for ka in self.kas:
            total += self.kas[ka].topic_coverage()
            kas += 1

        covered = 0
        for topic in self.topics:
            covered += topic.coverage()
        if covered:
            total += covered / len(self.topics)
            kas += 1
        if kas:
            return total / kas

        return 0

class Standard:
    """Represents an external standard for curriculum content and objectives"""
    def __init__(self, xmlfile, id):
      dt = ET.parse(xmlfile).getroot()
      self.id = id
      self.name = dt.find(ns + 'name').text
      self.body = dt.find(ns + 'body').text
      self.version = dt.find(ns + 'version').text
      self.url = dt.find(ns + 'documentUrl').text
      self.kas = {}
      for kat in dt.findall(ns + 'knowledgeArea'):
        ka = KnowledgeArea(kat, None, id)
        self.kas[ka.id] = ka

    def outcome_coverage_lookup(self, coverage):
      return self.outcome_lookup(coverage['knowledgeArea'].split('/'), int(coverage['id']))

    def outcome_lookup(self, kas, oid):
      if kas and self.kas and kas[0] in self.kas:
        return self.kas[kas[0]].outcome_lookup(kas[1:], oid)

    def topic_coverage_lookup(self, coverage):
      return self.topic_lookup(coverage['knowledgeArea'].split('/'), coverage['id'].split('/'))

    def topic_lookup(self, kas = (), topics = ()):
      if kas and self.kas and kas[0] in self.kas:
        return self.kas[kas[0]].topic_lookup(kas[1:], topics)

    def add_coverage(self, syllabus):
      """adds coverage from syllabus to each topic/outcome"""
      for ka in self.kas:
          self.kas[ka].add_coverage(syllabus)

    def outcome_coverage(self):
      total = 0
      for ka in self.kas:
          total += self.kas[ka].outcome_coverage()
      return total / len(self.kas)

    def topic_coverage(self):
      total = 0
      for ka in self.kas:
          total += self.kas[ka].topic_coverage()
      return total / len(self.kas)

class ConjunctiveRequirement:
    def __init__(self, ay, dt):
        self.courses = []
        for courset in filter(lambda n: n.tag == ns + 'course', dt):
          course = load_syllabus(ay, courset.find(ns + 'subject').text, courset.find(ns + 'number').text)
          self.courses.append(course)

    def max_hours(self):
        total = 0
        for course in self.courses:
            total += course.credit_hours
        return total


    def min_hours(self):
        total = 0
        for course in self.courses:
            total += course.credit_hours
        return total

class DisjunctiveRequirement:
    def __init__(self, ay, dt):
        self.courses = []
        self.conjunctions = []
        for courset in filter(lambda n: n.tag == ns + 'course', dt):
          course = load_syllabus(ay, courset.find(ns + 'subject').text, courset.find(ns + 'number').text)
          self.courses.append(course)
        for conjunctiont in dt.findall(ns + 'conjunction'):
          self.conjunctions.append(ConjunctiveRequirement(ay,conjunctiont))

    def max_hours(self):
        max = 0
        for course in self.courses:
            if course.credit_hours > max:
                max = course.credit_hours

        for conjunction in self.conjunctions:
            if conjunction.max_hours() > max:
                max = conjunction.max_hours()
        return max


    def min_hours(self):
        min = 1000000
        for course in self.courses:
            if course.credit_hours < min:
                min = course.credit_hours

        for conjunction in self.conjunctions:
            if conjunction.min_hours() < min:
                min = conjunction.min_hours()
        return min

    def available_courses(self):
        courses = set(self.courses)
        for conjunction in self.conjunctions:
            courses.update(conjunction.courses)
        return courses

class ProgramRequirement:
    def __init__(self, ay, dt):
        self.courses = []
        self.disjunctions = []
        for courset in filter(lambda n: n.tag == ns + 'course', dt):
          course = load_syllabus(ay, courset.find(ns + 'subject').text, courset.find(ns + 'number').text)
          self.courses.append(course)
        for disjunctiont in dt.findall(ns + 'disjunction'):
          self.disjunctions.append(DisjunctiveRequirement(ay,disjunctiont))

    def max_hours(self):
        total = 0
        for course in self.courses:
            total += course.credit_hours

        for disjunction in self.disjunctions:
            total += disjunction.max_hours()

        return total

    def min_hours(self):
        total = 0
        for course in self.courses:
            total += course.credit_hours

        for disjunction in self.disjunctions:
            total += disjunction.min_hours()

        return total

    def available_courses(self):
        courses = set(self.courses)
        for disjunction in self.disjunctions:
            courses.update(disjunction.available_courses())
        return courses

class ProgramSection:
    def __init__(self, ay, dt):
      self.requirements = []
      self.blanks = []
      for requirementt in dt.findall(ns + 'requirement'):
        self.requirements.append(ProgramRequirement(ay, requirementt))
      for blankt in dt.findall(ns + 'blank'):
        self.blanks.append(int(blankt.text))


    def max_hours(self):
      total = 0
      for requirement in self.requirements:
          total += requirement.max_hours()
      
      for blank in self.blanks:
        total += blank
      return total

    def min_hours(self):
      total = 0
      for requirement in self.requirements:
          total += requirement.min_hours()

      for blank in self.blanks:
        total += blank
      return total

    def available_courses(self):
        courses = set()
        for requirement in self.requirements:
            courses.update(requirement.available_courses())
        return courses

class Program:
    def __init__(self, ay, xmlfile):
      dt = ET.parse(xmlfile).getroot()
      self.name = dt.attrib['name']
      self.parent = load_program(ay, dt.attrib['parent']) if 'parent' in dt.attrib else None
      self.sections = []

      for sectiont in dt.findall(ns + 'section'):
        self.sections.append(ProgramSection(ay, sectiont))

    def max_hours(self):
        total = self.parent.max_hours() if self.parent else 0
        for section in self.sections:
            total += section.max_hours()
        return total

    def min_hours(self):
        total = self.parent.min_hours() if self.parent else 0
        for section in self.sections:
            total += section.min_hours()
        return total

    def available_courses(self):
        """returns syllabi for all courses that can be taken for credit within this program"""
        courses = set() if not self.parent else self.parent.available_courses()
        for section in self.sections:
            courses.update(section.available_courses())
        return courses


class Syllabus:
    """ Creates a class for each syllabi. These consist of a title, subject, course number, when it is offered
      the workload hours, the schedule type, the course description, course prerequisites, course objectices,
      and course topics"""
    def __init__(self, ay, xmlfile):
      """ parses the XML file and collects the information which includes title, subject, number, workload hours,
       offered, and what semester offered """
      dt = ET.parse(xmlfile).getroot()
      self.title = dt.find(ns + 'title').text
      self.ay = ay
      self.subject = dt.find(ns + 'subject').text
      self.number = dt.find(ns + 'number').text
      self.credit_hours = \
              (int(dt.attrib['creditHoursLecture']) if 'creditHoursLecture' in dt.attrib else 3) + \
              (int(dt.attrib['creditHoursLab']) if 'creditHoursLab' in dt.attrib else 0) + \
              (int(dt.attrib['creditHoursOther']) if 'creditHoursOther' in dt.attrib else 0) 
      self.workload_hours = int(3 if not 'workloadHoursLecture' in dt.attrib else dt.attrib['workloadHoursLecture'])
      if 'workloadHoursExpected' in dt.attrib:
          self.workload_hours = int(dt.attrib['workloadHoursExpected'])
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
      self.objectives = list()
      for objlist in dt.findall(ns + 'objectives'):
        for objectivet in objlist.findall(ns + 'objective'):
          self.objectives.append(Outcome(objectivet, len(self.objectives)+1))
      self.topics = list()
      for outline in dt.findall(ns + 'outline'):
        for topict in outline.findall(ns + 'topic'):
          self.topics.append(Topic(topict, str(len(self.topics)+1)))
    
    def get_topic_coverages(self):
        coverages = {}
        queue = self.topics
        while queue:
            # pop off topic
            topic = queue[0]
            queue = queue[1:]
            # update coverages
            coverages[topic.id] = topic.coverages
            # queue up subtopics
            queue.extend(topic.subtopics)
        return coverages

    def get_outcome_coverages(self):
        coverages = {}
        for outcome in self.objectives:
            coverages[outcome.id] = outcome.coverages
        return coverages

class Section:
    def __init__(self,course,section,instructorId,maxEnrollment,startTime=None,endTime=None,days=[],building=None,room=None,workloadHours=None):
        self.course = course
        self.section = section
        self.instructorId = instructorId
        self.maxEnrollment = maxEnrollment
        self.startTime = startTime
        self.endTime = endTime
        self.days = days
        self.building = building
        self.room = room
        self.workload_hours = workloadHours if workloadHours else course.workload_hours

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

def load_program(ay,name):
    program = Program(ay, open(resource_filename('mwsu_curriculum', 'programs/'+ay+'/'+name+'.xml')) )
    return program 


def load_programs(ay):
    assert path.exists(resource_filename('mwsu_curriculum', 'programs/'+ay)), "no programs for academic year " + ay + ' - bad path: ' + resource_filename('mwsu_curriculum', 'programs/'+ay)
    programs = {}
    for filename in next(walk(resource_filename('mwsu_curriculum', 'programs/'+ay)))[2]:
        program_name = filename[0:-4]
        programs[program_name] = load_program(ay, program_name)
    return programs


def load_standard(name, ay=None):
    standard = Standard(open(resource_filename('mwsu_curriculum', 'standards/'+name+'.xml')), name)
    if ay:
      for syllabus in load_syllabi(ay):
         standard.add_coverage(syllabus)
    return standard

def load_standards():
    standards = {}
    for filename in next(walk(resource_filename('mwsu_curriculum', 'standards/')))[2]:
        standards[filename[0:-4]] = Standard(open(resource_filename('mwsu_curriculum', 'standards/' + filename)) ,filename[0:-4])
    return standards

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
            workload_hours = float(sectiont.attrib['workloadHoursExpected']) \
                    if 'workloadHoursExpected' in sectiont.attrib else course.workload_hours
            daysList = list()
            for days in sectiont.findall(ns + 'day'):
                day = days.text
                daysList.append(day)
            section = Section(course,sectionNumber,instructorId,maxEnrollment,days=daysList, workloadHours=workload_hours,
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


def courses_in_semester(ay, qsemester):
    """ goes through all the courses and adds up the hours per semester """
    # update to use credit hours instead of # of courses
    semesters = defaultdict(list)
    for course in load_syllabi(ay):
        for semester in course.offered:
            semesters[semester].append(course)
    if qsemester == 'su':
        qsemester = 'summer'
    elif qsemester == 'fa':
        if int(ay[-2:]) % 2 == 1: # spring is odd, thus fall is even
            qsemester = 'fall-even'
        else:
            qsemester = 'fall-odd'
    else:
        if int(ay[-2:]) % 2 == 0:
            qsemester = 'spring-even'
        else:
            qsemester = 'spring-odd'

    return set(map(lambda course: course.subject + str(course.number), semesters[qsemester]))

