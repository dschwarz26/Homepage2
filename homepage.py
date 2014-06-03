import os
import webapp2
import jinja2
import logging
from update_files import Entry

JINJA_ENVIRONMENT = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions = ['jinja2.ext.autoescape'],
  autoescape = True)

class Homepage(webapp2.RequestHandler):

  def get(self):

    projects = [
      'github.com/dschwarz26/PokerBots',
    ]
    links = [
      'www.keithschwarz.com',
    ]

    template = JINJA_ENVIRONMENT.get_template('homepage.html')
    template_values = {
      'essays': Entry.query(Entry.category == 'essay').fetch(),
      'biopics': Entry.query(Entry.category == 'biopic').fetch(),
      'personals': Entry.query(Entry.category == 'personal').fetch(),
      'links': links,
      'projects': projects
      }
    self.response.write(template.render(template_values))

class Essaypage(webapp2.RequestHandler):

  def get(self, title):
    template = JINJA_ENVIRONMENT.get_template('essay.html')
    
    entries = Entry.query(Entry.title == title).fetch()
    if entries:
      entry = entries[0]
      template_values = {
        'title': entry.title,
        'published_date': entry.published_date,
        'content': entry.content
      }
      self.response.write(template.render(template_values))
    else:
      self.response.write('Entry with title %s not found' % title)

application = webapp2.WSGIApplication([
  ('/', Homepage),
  ('/essay/(\.*)', Essaypage),
], debug = True)

logging.getLogger().setLevel(logging.DEBUG)
