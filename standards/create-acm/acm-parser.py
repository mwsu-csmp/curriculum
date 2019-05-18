from html.parser import HTMLParser
import re
from collections import defaultdict

def to_acro(str):  # transform a sub-knowledge-area name in to an identifer
  acro = ''
  for c in str.strip().split(' '):
    if c:
      acro = acro + c.upper()[0]
  return acro

class ACMHTMLParser(HTMLParser):
    subkas = defaultdict(set)
    ka = None
    importance = None
    body = ''
    intopic = False
    ignore = False

    def restart_component(self):
      if self.intopic:
        print('      </topic>')
      self.intopic = False
      self.body = ''

    def restart_subka(self):
      self.restart_component()
      self.importance = None
      print('    </knowledgeArea>')

    def restart_ka(self):
      self.restart_subka()
      self.ka = None
      print('  </knowledgeArea>')
      
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
          self.ignore = True
        elif not self.ignore and tag == 'p': #beginning of chunk
          self.body = ''

    def handle_endtag(self, tag):
        if tag == 'table':
          self.ignore = False
        elif not self.ignore and tag == 'p':  # end of a significant chunk
          chunk = self.body.strip()

          if re.search('^(\w+)\/(.+)$', chunk): # parse new knowledge area
            ka, subkaname = re.search('^(\w+)\/(.+)$', chunk).groups()

            # find ID for subka (make sure it's not a duplicate)
            subka = to_acro(subkaname)
            i = 1
            while (subka if i==1 else subka+str(i)) in self.subkas[ka]:
              i = i + 1
            subka = subka if i==1 else subka+str(i)
            self.subkas[ka].add(subka)

            if self.ka: # end last nested KA
              if self.ka != ka:
                self.restart_ka()
              else:
                self.restart_subka()

            if self.ka == None or self.ka != ka: # start full KA
              print('  <knowledgeArea id=\'', ka, '\'>', sep='')
          
            self.ka = ka
            print('    <knowledgeArea id=\'',subka,'\' name=\'', subkaname, '\'>', sep='')
          elif chunk and chunk[0] in ('o', '•'): # parse a topic
            while chunk:  # these chunks sometimes contain multiple subtopics since not all subtopics are separated by <p> tags
              topic = chunk[1:]
              nextchunk = ''
              if re.search('\s+o\s+', topic):
                topic, nextchunk = re.search('^.(.*)\s+o\s+(.*)$', topic).groups()
                topic = topic.strip()
              if chunk[0] == 'o':
                print('        <topic>', topic, '</topic>', sep='')
              else:
                self.restart_component()
                self.intopic = True
                print('      <topic importance=\'', self.importance,'\'>', topic, sep='')  
              chunk = nextchunk.strip()
          elif re.search('^(\d+)\.\s*(.+)\s*\[(\w+)\]$', chunk):  # parse an outcome
            num, outcome, mastery = re.search('^(\d+)\.\s*(.+)\s*\[(\w+)\]$', chunk).groups()
            self.restart_component()
            print('      <outcome importance=\'', self.importance,'\' mastery_level=\'',mastery.lower(),'\'>', outcome, '</outcome>', sep='')
             
          else:
            pass # debug here if something is missing
          self.body = ''

    def handle_data(self, data):
        if self.ignore:  #don't read anything in a table tag
          pass
        elif re.search("(-\s*\d+)|(\d+\s*-)|(^\s*-\s*$)", data):  #skip page numbers
          pass
        elif re.search('Core-Tier1', data): #switch importance
          self.importance = 'tier1'
        elif re.search('Core-Tier2', data): #switch importance
          self.importance = 'tier2'
        elif re.search('Elective', data): #switch importance
          self.importance = 'elective'
        else: # data to add to the next chunk
          self.body = self.body + ' ' + data

parser = ACMHTMLParser()
intro = """  
<?xml version="1.0" encoding="UTF-8"?>
<curriculumStandard 
                    name="Computer Science Curricula"
                    body="acm"
                    version="2013" 
                    documentUrl="https://www.acm.org/binaries/content/assets/education/cs2013_web_final.pdf"
                    >"""
print(intro)
with open('input.html') as f:
    parser.feed(f.read())
print('</curriculumStandard>')
