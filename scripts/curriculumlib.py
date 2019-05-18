import xml.etree.ElementTree as ET

class Syllabus:
  title = None
  subject = None
  number = None
  
def parse_syllabus(xmlfile):
  ns = '{https://csmp.missouriwestern.edu}'
  dt = ET.parse(xmlfile).getroot()
  syllabus = Syllabus()
  
  syllabus.title = dt.find(ns+'title').text
  syllabus.subject = dt.find(ns+'subject').text
  syllabus.number = dt.find(ns+'number').text
  return syllabus
  
