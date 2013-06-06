try:
 from HTMLParser import HTMLParser
except ImportError:
 from html.parser import HTMLParser
import re
try:
 import htmlentitydefs as entities
except ImportError:
 from html import entities

__version__ = 0.1
__doc__ = """Strip html down to text in various ways."""

def strip_html_entities(s):
 """Converts any html entities in s to their unicode-decoded equivalents and returns a string."""
 if s is None:
  s = ''
 entity_re = re.compile(r"&(#\d+|\w+);")
 def matchFunc(match):
  """Nested function to handle a match object.
 If we match &blah; and it's not found, &blah; will be returned.
 if we match #\d+, unichr(digits) will be returned.
 Else, a unicode string will be returned."""
  if match.group(1).startswith('#'): return unichr(int(match.group(1)[1:]))
  replacement = entities.entitydefs.get(match.group(1), "&%s;" % match.group(1))
  return replacement.decode('iso-8859-1')
 return unicode(entity_re.sub(matchFunc, s))

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = re.sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def extract_text(html):
 if html is None:
  html = ''
 parser = _DeHTMLParser()
 parser.feed(html)
 parser.close()
 return parser.text()
    