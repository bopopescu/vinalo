# -*- coding: utf-8 -*-

from db import MyDB
from unidecode import unidecode
import re
from unicodedata import normalize
from slugify import slugify
from mysql.connector.errors import ProgrammingError
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

class ObjectTag:
    objectId = ""
    objectType = 8
    tagId = ""
    db = MyDB()

    def insertNewObjectTag(self,objectId,tagId):
        self.db.query("set names utf8;", None) 
        try:
            query = "INSERT INTO object_tag (object_id,object_type,tag_id) VALUES (%s,%s,%s)"
            self.db.query(query, (objectId,self.objectType,tagId))
            self.db._db_connection.commit()
            return self.db.getLastId()
        except UnicodeDecodeError as err:
            print "insert object tag error: ", err
            print self.db._db_cur._executed
        return None

# tag = ObjectTag()
# id = tag.insertNewObjectTag(37,2)
# print(id)