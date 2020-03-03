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
    ka = 0
    topic = 0
    ku = 0
    zone = None
    col = None
    kucont = None
    skip = True

    def handle_starttag(self, tag, attrs):
        left = 0
        if tag == 'div':
            groups = re.search('left:(\d+)\.', attrs[0][1])
            if groups:
                left = int(groups[1])
            else:
                left = 0
            if left >= 0 and left < 120:
                self.col = 1
            elif left > 120 and left < 270:
                self.col = 2
            elif left > 270 and left < 450:
                self.col = 3
            else:
                self.col = None
        if tag != 'span':
          self.zone= None
        else:
            c = attrs[0][1]
            if c == 'cls_030':
                self.zone = 'ka'
            if c == 'cls_015' and self.col == 1:
                self.zone = 'ku'
            if c == 'cls_015' and self.col == 2:
                self.zone = 'topic'
            if c == 'cls_036' and self.col == 2:
                self.zone = 'divider'

    def handle_endtag(self, tag):
        self.zone= None

    def handle_data(self, data):
        if data.endswith("Essentials and Learning Outcomes"):
                self.skip = True
                self.outcomes= True
                self.topic = 0
                print("    </knowledgeArea>");
        elif self.zone == 'ka':
            self.skip = False
            self.outcomes = False
            if self.ka > 0:
                print("  </knowledgeArea>");
            self.ka += 1 
            self.ku = 0
            print("  <knowledgeArea name=\"" + data + "\"  id=\"" + str(self.ka) + "\">")
        elif self.zone == 'ku' and len(data) > 2 and not self.skip and not self.outcomes:
            if data.endswith('and'):
                self.kucont = data
            else:
                if self.kucont:
                    data = self.kucont + ' ' + data
                    self.kucont = None
                if self.ku > 0:
                    print("    </knowledgeArea>");
                self.ku += 1
                self.topic = 0
                print("    <knowledgeArea name=\"" + data + "\" id=\"" + str(self.ku) + "\" >")
        elif self.zone == 'topic' and len(data) > 2 and not self.skip and not self.outcomes:
            self.topic += 1
            print("      <topic>" + data + "</topic>")
        elif self.zone == 'topic' and len(data) > 2 and self.outcomes:
            self.topic += 1
            print("    <outcome>" + data + "</outcome>")

parser = ACMHTMLParser()
intro = """  
<curriculumStandard
  xmlns="https://csmp.missouriwestern.edu"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="https://csmp.missouriwestern.edu/xml/curriculum/standard.xsd">

 <name>Cybersecurity Curricula</name>
 <body>acm</body>
 <version>2017</version>
 <documentUrl>https://cybered.hosting.acm.org/wp-content/uploads/2018/02/newcover_csec2017.pdf</documentUrl>
"""
print(intro)
with open('cyber2017-2.html') as f:
    parser.feed(f.read())
print('  </knowledgeArea>')
print('</curriculumStandard>')
