from os import listdir
import datetime
import logging
from google.appengine.ext import ndb

class Entry(ndb.Model):
  title = ndb.StringProperty()
  category = ndb.StringProperty()
  publish_date = ndb.DateProperty()
  content = ndb.TextProperty()
  rank = ndb.IntegerProperty()

#Reads the .txt files in the static folder, creates models from them,
#and writes them to the db.
base_path = '/home/daniel/Homepage/content'

essay_order = [
  'Beckoning',
  'Dislocated Priors',
  'Misguided but Effective Heuristics',
  'Utility Swaps',
  'In Defense of Eating Meat',
  'More on Ethics of Vegetarianism',
  'Virtue Ethics',
  'A Job Well Done',
  'A Life Well Lived',
  'On Categorizing Errors of Reasoning',
  'Unpacking',
  'Global Maxima',
  'A Simple Case of Updating'
]

biopic_order = [
  'Nassim Taleb',
  'Sam Harris',
  'Christopher Hitchens',
  'Ludwig Wittgenstein'
]

personal_order = [
  'My Grandma Janet',
  'A Difficult Life Transition',
  'Singularity Summit 2012',
  'Lessons from 2010, 2011',
  'Nootropics'
]
    
def run():
    read_in_entries(essay_order, '/essays/', 'essay')
    read_in_entries(biopic_order, '/biopics/', 'biopic')
    read_in_entries(personal_order, '/personals/', 'personal')
    logging.info('Content updated.')

def read_in_entries(entry_order, entry_dir, category):
    path = base_path + entry_dir
    for f in listdir(path):
        o = open(path + f, 'rb')
        date_tokens = o.readline().split('-')
        name = f[:-4]
        existingEntries = Entry.query(Entry.title == name.replace(' ', '')).fetch()
        if existingEntries:
          existingEntry = existingEntries[0]
          existingEntry.content = o.read()
          existingEntry.rank = entry_order.index(name)
          existingEntry.put() 
        else:
          try:
            entry = Entry(
              title = name.replace(' ', ''),
              category = category,
              publish_date = datetime.date(int(date_tokens[0]), int(date_tokens[1]), int(date_tokens[2])),
              content = o.read(),
              rank = entry_order.index(name))
          except ValueError:
            logging.error('Entry %s not in list' % name)
          entry.put()

