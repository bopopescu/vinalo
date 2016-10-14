# -*- coding: utf-8 -*-

from db import MyDB
from unidecode import unidecode
import re
from unicodedata import normalize
from slugify import slugify

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

# def slugify(text, delim=u'-'):
#     """Generates an slightly worse ASCII-only slug."""
#     result = []
#     for word in _punct_re.split(text.lower()):
#         word = normalize('NFKD', word).encode('ascii', 'ignore')
#         if word:
#             result.append(word)
#     return unicode(delim.join(result))

class City:
    id = ""
    name = ""
    sid = ""
    db = MyDB()

    def getIdCityFromName(self,name):
        query = "SELECT * FROM city_province WHERE name LIKE '%s'" %('%'+name+'%')
        self.db.query(query,(name))
        data = self.db._db_cur.fetchone()
        if data != None and data.count > 0:
            return data[0]
        return 0

    def getIdProvinceFromCity(self,cityId,name):
        self.db.query("set names utf8;", None)
        query = "SELECT * FROM district WHERE city_id = %s AND name LIKE %s"
        try:
            self.db.query(query,(cityId,name))
            data = self.db._db_cur.fetchone()
            if data != None and data.count > 0:
                return data[0]
            
            #insert new district to city
            return self.insertNewDistrict(cityId,name)
        except UnicodeDecodeError as err:
            print err
            print self.db._db_cur._executed
            #insert new district to city
            return self.insertNewDistrict(cityId,name)

    def insertNewDistrict(self,cityId,name):
        alias = self.makeAlias(name)
        self.db.query("set names utf8;", None) 
        try:
            query = "INSERT INTO district (city_id,name,alias) VALUES (%s,%s,%s)"
            self.db.query(query, (cityId,name,alias))
            self.db._db_connection.commit()
            return self.db.getLastId()
        except UnicodeDecodeError as err:
            print "insert district error: ", err
            print self.db._db_cur._executed
        return None

    def makeAlias(self,name):
        name = name.replace(u'đ', u'd')
        try:
            txt = slugify(name)
            return txt
        except UnicodeEncodeError as err:
            print err
            print name
        return ""


# city = City()
# id = city.getIdCityFromName(u"Hồ Chí Minh")
# province = city.getIdProvinceFromCity(id, "Quận Phú Nhuận")
# print(province)