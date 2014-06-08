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
      {
        'name': 'Poker Simulator',
        'link': 'poker-simulator.appspot.com'
      },
      {
        'name': 'Chess Notifier',
        'link': 'chessnotifier.appspot.com'
      },
      {
        'name': 'Bitcoin Prediction Trader',
        'link': 'predictiousbot.appspot.com'
      },
      {
        'name': 'Homepage Source',
        'link': 'https://github.com/dschwarz26/Homepage2'
      }, 
    ]

    links = [
      {
        'name': 'Facebook',
        'link': 'https://www.facebook.com/daniel.schwarz.735'
      },
      {
        'name': 'Twitter',
        'link': 'https://twitter.com/dschwarz26'
      },
      {
        'name': 'LinkedIn',
        'link': 'https://www.linkedin.com/profile/view?id=192589584'
      },
      {
        'name': 'Github',
        'link': 'https://github.com/dschwarz26'
      },
      {
        'name': 'Keith Schwarz',
        'link': 'http://www.keithschwarz.com'
      },
      {
        'name': 'Joseph Schwarz',
        'link': 'http://www.josephschwarz.com'
      }
    ]

    template = JINJA_ENVIRONMENT.get_template('homepage.html')
    template_values = {
      'essays': Entry.query(Entry.category == 'essay').order(Entry.rank).fetch(),
      'biopics': Entry.query(Entry.category == 'biopic').order(Entry.rank).fetch(),
      'personals': Entry.query(Entry.category == 'personal').order(Entry.rank).fetch(),
      'links': links,
      'projects': projects
      }
    self.response.write(template.render(template_values))

class Entrypage(webapp2.RequestHandler):

  def get(self, title):
    template = JINJA_ENVIRONMENT.get_template('entry.html')
    
    entries = Entry.query(Entry.title_no_spaces == title).fetch()
    if entries:
      entry = entries[0]
      template_values = {
        'title': entry.title,
        'published_date': entry.publish_date,
        'content': entry.content
      }
      self.response.write(template.render(template_values))
    else:
      self.response.write('Entry with title %s not found' % title)

application = webapp2.WSGIApplication([
  ('/', Homepage),
  ('/essay/(\w+)', Entrypage),
  ('/personal/(\w+)', Entrypage),
  ('/biopic/(\w+)', Entrypage),
], debug = True)

logging.getLogger().setLevel(logging.DEBUG)
