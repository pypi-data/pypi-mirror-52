import sqlite3

class dingdb():

  def __init__(self, database='./data.db'):
    """Initalise connection
    :args: database - full path to sqlite database
    """
    self.database = database


  def getdb(self):
    """Return database connection"""
    conn = sqlite3.connect(self.database)
    conn.row_factory = sqlite3.Row
    return conn

  def help():
    print("""Usage: 
      - getDing(id)
      - putDing(7, 'person', 'person', data=[{'key':'name', 'value': 'Sam'}, {'key':'age', 'value':30}])
      - getDingsByType(kind_id)
      
    """)

  def getDing(self, id):
    db = self.getdb()
    c = db.cursor()
    c.execute(
    """
    SELECT DISTINCT
    ding.id, ding.name, ding.kind_id,
    data.version_id, data.key, data.value
    from data
     join version on 
      data.ding_id = version.ding_id
     join ding on
      version.ding_id = ding.id
    where data.ding_id = ?
    """, (id,))
    result = c.fetchall()
    db.close()
    # Build a ding
    rawDing = {
    'id': result[0]['id'],
    'kind': result[0]['kind_id'],
    'name': result[0]['name'],
    'data': {}
    }
    for row in result:
      rawDing['data'][row['key']] = row['value']
    # Return ding
    return ding(rawDing)

  def getDingsByType(self, kind_id):
    """Return list of dings of a given type"""
    db = self.getdb()
    c = db.cursor()
    c.execute(
      """
      SELECT DISTINCT
      ding.id, ding.name, ding.kind_id,
      data.version_id, data.key, data.value
      FROM data
       JOIN version ON
        data.ding_id = version.ding_id
       JOIN ding ON
        version.ding_id = ding.id
      WHERE ding.kind_id = ?
      GROUP BY data.ding_id, data.key
      ORDER BY ding.id

    """, (kind_id,))
    result = c.fetchall()
    db.close()
    # Build dings list
    dings = {} #Dict
    for row in result:
      currentId = row['id']
      if currentId not in dings:
        dings[currentId] = {}
      dings[currentId]['kind'] = row['kind_id']
      if 'data' not in dings[currentId]:
        dings[currentId]['data'] = {}
      # Apply attributes
      dings[currentId]['data'][row['key']] = row['value']
   
    return dings

  def putDing(self, ding_id, name, kind_id, data=None, creator=None, creation_date=None, comment=None):
    db = self.getdb()
    c = db.cursor()
    c.execute(
    """
    INSERT INTO ding (id, name, kind_id) VALUES (?, ?, ?)
    """, (ding_id, name, kind_id))

    c.execute(
    """
    INSERT INTO version (id, ding_id, creator, creation_date,comment) VALUES (?, ?, ?, ?, ?)
    """, (0, ding_id, creator, creation_date, comment))
    
    for attribute in data:
      c.execute(
      """
      INSERT INTO data (version_id, ding_id, key, value) VALUES(?, ?, ?, ?)
      """, (0, ding_id, attribute['key'], attribute['value']))
    # Commit all 
    db.commit()

  def deleteDing(self, ding_id):
    db = self.getdb()
    c = db.cursor()
    c.execute(
    """
    DELETE FROM ding WHERE id=?
    """, (ding_id,))

    c.execute(
    """ 
    DELETE FROM version WHERE ding_id = ?;
    """, (ding_id,))
    db.commit()

class ding(dingdb):
  def __init__(self, rawDing):
    super().__init__()
    self.ding = rawDing
  
  def load(self):
    """Return ding object"""
    return self.ding

  def save(self):
    """Persist latest ding to the database"""
    # Refresh attributes - if an attribute never gets explicitly set, its not available
      # TODO understand why we need to refesh them...
    for key in self.ding['data'].keys():
      try:
        self.ding['data'][key] = self.__getattribute__(key) 
      except AttributeError:
        self.__setattr__(key, self.ding['data'][key])

    for key in self.ding['data'].keys():
      db = self.getdb()
      c = db.cursor()
      c.execute(
      """
      INSERT INTO data (ding_id, version_id, key, value)
      VALUES (?, ?, ?, ?)
      """,(self.ding['id'], 0, key, self.__getattribute__(key)))
      db.commit()

  def __getattr__(self, attribute):
    return self.__dict__['ding']['data'][attribute]
    

