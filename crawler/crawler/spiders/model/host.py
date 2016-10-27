# -*- coding: utf-8 -*-

import scrapy
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
from tag import Tag
from objectTag import ObjectTag
# from PIL import Image

class Host():
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
    viewMap = 0
    crawler = ""
    suffixId = ""
    db = MyDB()
    listTagId = []

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
        self.crawler = data[22]

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

        self.listTagId = []
        tag = Tag()
        #khung gia: 2tr -10tr
        rows = hxs.xpath('//div[@class="rdct_0"]/table/tr').extract()
        for row in rows:
            listTd = Selector(text=row).xpath('//td/p/text()').extract()
            if len(listTd) > 0:
                left = listTd[0]
                listTd = Selector(text=row).xpath('//td/b/text()').extract()
                right = listTd[0]

                if left.find(u'giá') > 0:
                    self.tag = right
                    self.listTagId.append(tag.getIdTagFromName(self.tag, 16339))

        rows = hxs.xpath('//div[@class="rdct_0"]/table/tr/td/div/p[@class="imgtiddtt"]/text()').extract()
        # print 'haha'
        # print rows
        for idx,row in enumerate(rows):
            if row == u'Tiện ích':
                xpath = '//div[@class="rdct_0"]/table/tr/td/div'
                rr = hxs.xpath(xpath).extract()
                rrr = Selector(text=rr[idx]).xpath('//p[@class="bleftdd_1"]/a/text()').extract()
                # print rrr
                for r in rrr:
                    t = r.strip()
                    if t != u'Khác':
                        self.tag += ',' + t
                        self.listTagId.append(tag.getIdTagFromName(t, 16359))
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
            # print "districtId=",self.districtId
            # print self.districtId


    def insertDB(self):
        self.db.query("set names utf8;", None) 
        query = "INSERT INTO host (name,description,address,phone,image_profile,longtitude,lattitude,website,alias,type_id,tag,district_id,starttime,endtime,crawler,view_map)" \
        " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
            self.suffixId,
            self.viewMap))
            self.db.commit()
            # print self.db._db_cur._executed
            return self.db.getLastId()
        except mysql.connector.Error as err:
            print err
            print self.db._db_cur._executed
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
            print err
        return False

    def getItems(self):
        query = "SELECT id,alias,crawler FROM host WHERE crawler != \"\" AND description LIKE '%s' ORDER BY `host`.`id` ASC"%("%đang cập nhật%")
        print query
        try:
            self.db.query(query, None)
            data = self.db._db_cur.fetchall()
            if data != None:
                return data
            return False
        except mysql.connector.Error as err:
            print err
        return False

    def getDescription(self, response):
        hxs = Selector(text=response.body)
        listDescription = hxs.css('h2.prcbdd1::text').extract()
        res = ""
        if len(listDescription):
            res = "\n".join(listDescription)
        print res
        return res

    def updateDescription(self, id, description):
        self.db.query("set names utf8;", None) 
        query = "UPDATE host SET description=%s WHERE id=%s"
        try:
            self.db.query(query, (description,id))
            self.db.commit()
            # print self.db._db_cur._executed
            return True
        except mysql.connector.Error as err:
            print err
            print self.db._db_cur._executed
        return False

    def getListHost(self,idx,limit):
        query = "SELECT id,alias,crawler,tag FROM host WHERE crawler != \"\" ORDER BY `host`.`id` ASC LIMIT %s,%s"%(idx,limit)
        try:
            self.db.query(query, None)
            data = self.db._db_cur.fetchall()
            if data != None:
                return data
            return False
        except mysql.connector.Error as err:
            print err
        return False

    def getKeyword(self, response):
        meta = response.meta

        id = meta['id']
        txtTag = meta['tag']

        hxs = Selector(text=response.body)
        rows = hxs.xpath('//div[@class="rdct_0"]/table/tr/td/div/p[@class="imgtiddtt"]/text()').extract()

        tag = Tag()
        objectTag = ObjectTag()
        listTagId = []

        # list tag
        for idx,row in enumerate(rows):
            if row == u'Phục vụ các món':
                tag.patternTypeId = 7
                xpath = '//div[@class="rdct_0"]/table/tr/td/div'
                rr = hxs.xpath(xpath).extract()
                rrr = Selector(text=rr[idx]).xpath('//p[@class="bleftdd_1"]/a/text()').extract()
                for r in rrr:
                    t = r.strip()
                    if t != u'Khác':
                        txtTag += ',' + t
                        listTagId.append(tag.getIdTagFromName(t, 19454))

            if row == u'Phù hợp với mục đích':
                tag.patternTypeId = 0
                xpath = '//div[@class="rdct_0"]/table/tr/td/div'
                rr = hxs.xpath(xpath).extract()
                rrr = Selector(text=rr[idx]).xpath('//p[@class="bleftdd_1"]/a/text()').extract()
                for r in rrr:
                    t = r.strip()
                    if t != u'Khác':
                        txtTag += ',' + t
                        listTagId.append(tag.getIdTagFromName(t, 0))

        # print txtTag
        
        # update tag object
        for tagId in listTagId:
            if tagId > 0:
                # print id, tagId
                objectTag.insertNewObjectTag(id, tagId)

        self.updateKeyword(id,txtTag)

    def updateKeyword(self,id,txtTag):
        self.db.query("set names utf8;", None) 
        query = "UPDATE host SET tag=%s WHERE id=%s"
        try:
            self.db.query(query, (txtTag,id))
            self.db.commit()
            # print self.db._db_cur._executed
            return True
        except mysql.connector.Error as err:
            print err
            print self.db._db_cur._executed
        return False