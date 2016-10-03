# -*- coding: utf-8 -*-

from db import MyDB
from unidecode import unidecode
import re
from unicodedata import normalize

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

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
        query = "SELECT * FROM district WHERE city_id = %s AND name LIKE '%s'" %(cityId,'%'+name+'%')
        print(query)
        self.db.query(query,(name))
        data = self.db._db_cur.fetchone()
        if data != None and data.count > 0:
            return data[0]
        #insert new district to city
        return self.insertNewDistrict(cityId,name)

    def insertNewDistrict(self,cityId,name):
        alias = self.makeAlias(name)
        query = "INSERT INTO district (city_id,name,alias) VALUES ('%s','%s','%s')" %(cityId,name.decode('utf-8'),alias)
        print(query)
        self.db.query(query, None)
        self.db._db_connection.commit()
        return self.db.getLastId()

    def makeAlias(self,name):
        name = name.replace('đ', 'd')
        txt = slugify(name.decode('utf-8'))
        return txt

# city = City()
# id = city.getIdCityFromName(u"Đà Nẵng")
# province = city.getIdProvinceFromCity(id, "bá đạo haha3")
# print(province)