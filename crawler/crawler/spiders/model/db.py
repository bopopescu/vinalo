import mysql.connector
from mysql.connector import Error

class MyDB(object):
    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = mysql.connector.connect(host='localhost',
                               database='wassup',
                                   user='root',
                               password='root',
                               charset='utf8',use_unicode=True)
        self._db_cur = self._db_connection.cursor(buffered=True)

    def query(self, query, params):
        return self._db_cur.execute(query, params)

    def __del__(self):
        self._db_connection.close()

    def getLastId(self):
        return self._db_cur.lastrowid

    def commit(self):
      return self._db_connection.commit()

