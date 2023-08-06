# Dingdb, a thingdb like storage & retrieval Python API 

Simple implementation of **Thingdb**, called **Dingdb** (German for *'thing'*)
Currently expects a sqlite3 database.

Inspired by: 

- http://web.archive.org/web/20080109204022/http://pharos.infogami.com/tdb
- https://github.com/reddit-archive/reddit/blob/master/r2/r2/lib/db/ding.py
- https://github.com/itslukej/ding/tree/master/dingdb
- https://www.reddit.com/r/webdev/comments/30ycc1/has_anyone_built_a_reddit_clone_if_so_any_tips_on/
  - http://www.reddit.com/r/webdev/.json
- https://www.youtube.com/watch?v=hB-M8oH4K4w

# Installation

```
git clone git@github.com:chrisjsimpson/dingdb.git
cd dingdb/
pip3 install ./
python3 dingdb/migrations/1-create-dingdb-schema.py -up -db ./data.db
```

# Usage

```
from dingdb import dingdb
from uuid import uuid4

dingdb.help() # See help

# Connect and insert data
tdb = dingdb(database='./data.db')
# Put things
tdb.putDing(1, 'person', 'person', data=[{'key':'name', 'value': 'Sam'}, {'key':'age', 'value':30}])
# Get a thing
person = tdb.getDing(1)
person.name 
'Sam'
person.age
'30'
person.age = 31
person.save()

# Get things by type
tdb.getDingsByType('person')

# More..

# Use a uuid for ids:
tdb.putDing(str(uuid4()), 'person', 'person', data=[{'key':'name', 'value': 'Sam'}, {'key':'age', 'value':30}])
```
