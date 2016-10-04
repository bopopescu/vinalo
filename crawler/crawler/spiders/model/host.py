# -*- coding: utf-8 -*-

from unidecode import unidecode
import re
from unicodedata import normalize
from db import MyDB
import pprint
import urllib
from lxml.html import HTMLParser, fromstring
from scrapy.selector import Selector
from datetime import datetime
from city import City
import mysql.connector
from mysql.connector import Error
import logging

class Host:
    name = ""
    description = ""
    address = ""
    phone = ""
    image_profile = ""
    status = 1
    longtitude = ""
    lattitude = ""
    website = ""
    alias = ""
    typeId = ""
    created_at = ""
    creatorId = ""
    tag = ""
    districtId = ""
    startTime = "08:00:00"
    endTime = "21:00:00"
    viewMap = 1
    crawler = ""
    suffixId = ""
    db = MyDB()

    def parse(self, str):
        data = str.split("[0h0]")
        self.name = data[0]
        self.address = data[1]
        self.image_profile = data[2]
        location = data[19].split(',')
        self.lattitude = location[0]
        self.longtitude = location[1]
        self.suffixId = data[22]
        self.alias = data[12]

    def parseContent(self, response):
        hxs = Selector(text=response.body)
        try:
            self.phone = hxs.css('ul.textsdtdd li::text').extract()[0]
        except IndexError:
            pass

        try:
            self.website = hxs.css('p.topusc5_0::text').extract()[0]
        except IndexError:
            pass
        # print(self.website)

        rows = hxs.xpath('//div[@class="rdct_0"]/table/tr/td/b/text()').extract()
        if len(rows) > 0:
            time = rows[0]
            if time:
                try:
                    time = time.split('-')
                    t = time[0].strip()
                    dateObj = datetime.strptime(t, '%I:%M %p')
                    self.startTime = dateObj.strftime('%H:%M:%S')
                    # print self.startTime

                    t = time[1].strip()
                    dateObj = datetime.strptime(t, '%I:%M %p')
                    self.endTime = dateObj.strftime('%H:%M:%S')
                    # print self.endTime
                except (ValueError,IndexError):
                    pass

        if len(rows) >= 3:
            self.tag = rows[2].strip()

        rows = hxs.xpath('//div[@class="rdct_0"]/table/tr/td/div/p[@class="bleftdd_1"]/a/text()').extract()
        for row in rows:
            self.tag += ',' + row.strip()
        # print self.tag

        rows = hxs.xpath('//div[@class="ndungleftdct"]/div[@class="ndleft_0"]/p/text()').extract()
        if len(rows) > 0:
            self.description = rows[0]
        # print self.description

        meta = response.meta
        self.typeId = meta["typeId"]

        cityId = meta["cityId"]
        rows = hxs.xpath('//div[@class="rdct_0"]/p[@class="rdctfollow_0"]/span[@class="rdctfollow_5"]/text()').extract()
        if len(rows) == 3:
            district = rows[2][8:].strip()
            city = City()
            self.districtId = city.getIdProvinceFromCity(cityId, district)
            # print self.districtId


    def insertDB(self):
        self.db.query("set names utf8;", None) 
        query = "INSERT INTO host (name,description,address,phone,image_profile,longtitude,lattitude,website,alias,type_id,tag,district_id,starttime,endtime,crawler)" \
        " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.db.query(query, (self.name,
            self.description,
            self.address,
            self.phone,
            self.image_profile,
            self.longtitude,
            self.lattitude,
            self.website,
            self.alias,
            self.typeId,
            self.tag,
            self.districtId,
            self.startTime,
            self.endTime,
            self.suffixId))
            self.db.commit()
            # print self.db._db_cur._executed
            return self.db.getLastId()
        except mysql.connector.Error as err:
            logging.log(logging.ERROR, err)
            logging.log(logging.ERROR, self.db._db_cur._executed)
        return -1

    def checkExisted(self):
        query = "SELECT id FROM host WHERE alias LIKE '%s'"%(self.alias)
        try:
            self.db.query(query, None)
            data = self.db._db_cur.fetchone()
            if data != None:
                return True
            return False
        except mysql.connector.Error as err:
            logging.log(logging.ERROR, err)
        return False



