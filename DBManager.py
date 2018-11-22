import os.path
import sqlite3
class DBManager:
  def __init__(self, dbname="log.db"):
    self.conn = sqlite3.connect(dbname)
    self.c = None

  def addElements(self, jsonDict):
    self.c = self.conn.cursor()
    self.__initTables__(jsonDict)
    self.conn.commit()
    self.conn.close()
  
  def __initTables__(self, jsonDict):
    for key in jsonDict.keys():
      print "Creating and filling " + key
      self.__initTable__(key, jsonDict)
      self.__insertData__(key, jsonDict)

  def __initTable__(self, tablename, values):
    sql = "create table if not exists " + tablename + " (" + self.__getfieldsforcreation__(values[tablename]) + ")"
    self.c.execute(sql)

  def __insertData__(self, tablename, values):
    for value in values[tablename]:
      self.__insertRow__(tablename, value)

  def __insertRow__(self, tablename, value):
    return self.c.execute(self.__generateInsert__(tablename, value), self.__getValuesForInsert__(value)).lastrowid

  def __generateInsert__(self, tablename, value):
    ints = "?,"*len(value.keys())
    ints = ints[:-1]
    sql = "insert into " + tablename + " values (" + ints + ")"
    return sql

  def __getValuesForInsert__(self, value):
    aux = []
    for key in value.keys():
      if isinstance(value[key],dict):
        aux.append(self.__insertRow__(key, value[key]))
      else:
        aux.append(value[key])
    return tuple(aux)

  def __getfieldsforcreation__(self, values):
    fields = ""
    for key in values[0].keys():
      if isinstance(values[0][key],dict):
        self.__initTable__(key, {key:[values[0][key]]})
        fields += "id" + key + " integer,"
      else:
        fields += key + " text,"
    return fields[:-1]
    
