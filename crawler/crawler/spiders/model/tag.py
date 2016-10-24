# -*- coding: utf-8 -*-

from db import MyDB
from unidecode import unidecode
import re
from unicodedata import normalize
from slugify import slugify
from mysql.connector.errors import ProgrammingError
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

class Tag:
    id = ""
    tag = ""
    alias = ""
    parentId = ""
    patternTypeId = 3
    status = 1
    db = MyDB()

    def getIdTagFromName(self,name,parentId):
        self.db.query("set names utf8;", None)
        alias = self.makeAlias(name)
        query = "SELECT id FROM tag WHERE alias LIKE '%s'" % (alias)
        # try:
        self.db.query(query,None)
        data = self.db._db_cur.fetchone()
        if data != None:
            return data[0]
        
        #insert new district to city
        return self.insertNewTag(name,parentId)
        # except (UnicodeDecodeError,ProgrammingError) as err:
        #     print err
        #     print self.db._db_cur._executed
            #insert new district to city

    def insertNewTag(self,name,parentId):
        alias = self.makeAlias(name)
        self.db.query("set names utf8;", None) 
        try:
            query = "INSERT INTO tag (tag,alias,parent_id,pattern_type_id) VALUES (%s,%s,%s,%s)"
            self.db.query(query, (name,alias,parentId,self.patternTypeId))
            self.db._db_connection.commit()
            return self.db.getLastId()
        except UnicodeDecodeError as err:
            print "insert tag error: ", err
            print self.db._db_cur._executed
        return 0

    def makeAlias(self,name):
        name = name.replace(u'đ', u'd')
        try:
            txt = slugify(name)
            return txt
        except UnicodeEncodeError as err:
            print err
            print name
        return ""


# tag = Tag()
# id = tag.getIdTagFromName(u"Hồ Chí Minh 13")
# print(id)