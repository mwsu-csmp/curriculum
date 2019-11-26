import xml.etree.ElementTree as ET
from os import walk
from collections import defaultdict

class Standards:
  """ Creates class for Standards """
  knowledgeArea = None
  topic = None
  tier1 = None
  outcome = None
  name = None

def parse_standards(xmlfile):
  """ Goes through and collects information in selected standards xml file """
  ns = '{https://csmp.missouriwestern.edu}'
  tree = ET.parse(xmlfile)
  dt = tree.getroot()
  standards = Standards()

##parses the whole file
  for standards.knowledgeArea in dt.iter():
      knowledgeArea = print(standards.knowledgeArea.attrib, standards.knowledgeArea.text)
      tree.write('output.xml')
##selects the tier on topics.. this is a work in progress
##for standards.topic in dt.iter():
##    for topic in standards.topic.findall(".//*[@importance='tier1']"):
##       tier1 = print(topic.tag,topic.attrib, topic.text)

  standards.name = dt.find(ns+'name').text
  ##standards.knowledgeArea = dt.find(ns+'knowledgeArea').attrib
  ##standards.knowledgeAreaAttrib = standards.knowledgeArea


  return standards

def load_standards():
  """ Uses parse_standards for each xml file in standards folder """
  return [parse_standards(open('standards/'+filename)) for filename in next(walk('standards'))[2]]



