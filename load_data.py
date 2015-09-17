import zipfile, os.path, sys, re
import pymongo
from pymongo import MongoClient

dbhost = 'mongodb://localhost:27017'
# TODO: server-side mongo host
mongoclient = MongoClient(dbhost)
db = mongoclient.namestuff
db.person.create_index([('name', pymongo.ASCENDING), ('gender', pymongo.ASCENDING)], unique=True)
db.popularity.create_index([('person_id', pymongo.ASCENDING), ('year', pymongo.ASCENDING)], unique=True)

FILENAME_PATTERN = re.compile('yob(\d\d\d\d)\.txt')

def load_data(filename, dest_dir):
  unzip(filename, dest_dir)
  for filename in os.listdir(dest_dir):
    m = FILENAME_PATTERN.match(filename)
    year = None
    if m:
      print 'loading '+str(filename)
      year = int(m.group(1))
      with open(os.path.join(dest_dir, filename)) as f:
        lines = f.readlines()
        for line in lines:
          (name, gender, count) = line.strip().split(',')
          person = None
          #try:
          person = db.person.find_one({'name': name, 'gender': gender})
          person_id = None
          if not person:
            person_id = db.person.insert_one({'name': name, 'gender': gender}).inserted_id
          else:
            person_id = person['_id']
          db.popularity.insert_one({'person_id': person_id, 'year': year, 'count': int(count)})
          #except Exception as e:
          #  print e

def unzip(filename, dest_dir):
  with zipfile.ZipFile(filename) as zf:
    for member in zf.infolist():
      words = member.filename.split('/')
      path = dest_dir
      for word in words[:-1]:
        drive, word = os.path.splitdrive(word)
        head, word = os.path.split(word)
        if word in (os.curdir, os.pardir, ''):
          continue
        path = os.path.join(path, word)
      zf.extract(member, path)

def main(filename):
  dest_dir = './tmp'
  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
  load_data(filename, dest_dir)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    main(sys.argv[1])
  else:
    print 'not enough args'
