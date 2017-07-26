import mysql.connector
from mysql.connector import Error

class MyDB(object):
  _db_connection = None
  _db_cur = None

  def __init__(self):
    self._db_connection = mysql.connector.connect(host='172.17.0.3',
                database='truyentranh',
                user='truyentranh',
                password='123',
                charset='utf8',
                use_unicode=True)
    self._db_cur = self._db_connection.cursor(buffered=True,dictionary=True)

  def query(self, query, params=()):
    self._db_cur.execute(query, params)

  def fetchRow(self, query, params=()):
    self.query(query, params)
    return self._db_cur.fetchall()

  def fetchAll(self, query, params=()):
    self.query(query, params)
    return self._db_cur.fetchall()

  def commit(self):
    self._db_connection.commit()

  def __del__(self):
    pass
    # if self._db_connection != None:
    #   self._db_connection.close()

  def getLastId(self):
    return self._db_cur.lastrowid

  def commit(self):
    return self._db_connection.commit()

