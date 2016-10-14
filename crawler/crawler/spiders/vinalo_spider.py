# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
from scrapy.http import FormRequest
from model.host import Host
import pprint
import urllib
from lxml.html import HTMLParser, fromstring
from scrapy.selector import Selector
from datetime import datetime
from model.city import City
from model.objectTag import ObjectTag
from slugify import slugify

from scrapy.item import Item
from crawler.items import ImageItem
import hashlib

with open("city") as file:
    listCity = json.load(file)

with open('category') as file:
    listCate = json.load(file)


print len(listCate)

class VinaloSpider(scrapy.Spider):
    name = "vinalo"
    allowed_domains = ["vinalo.com"]
    start_urls = (
        'https://vinalo.com',
    )

    indexListCate = 0
    indexSId = 0
    indexCity = 0

    def start_requests(self):
        self.crawler.engine.slot.scheduler.df.fingerprints = set()

        print "index city", self.indexCity
        city = listCity[self.indexCity]
        yield scrapy.Request('https://vinalo.com/', 
                        cookies = {"tpvnl":city['sid']}, 
                        callback=self.readEachProvince,
                        meta = {"cityId":city['id'],"cityName":city["name"]},
                        dont_filter = True
        )

    def readEachProvince(self, response):
        url = 'https://vinalo.com/loadh/getddloai'
        data = {
            "lddc": "",
            "tidd": "",
            "atc": "",
            "lat": "10.81712",
            "lng": "106.627808",
            "ldd": "",
            "al": "3",
            "rt": "0",
        }
        meta = response.meta


        cate = listCate[self.indexListCate]
        sid = cate["sid"][self.indexSId]


        if self.indexSId < len(cate['lddc']):
            data['lddc'] = cate['lddc'][self.indexSId]


        print "index list cate", cate
        print "index sid", sid
        print "lddc", data['lddc']

        data['ldd'] = sid
        meta["data"] = data
        meta["typeId"] = cate["id"]
        meta["sid"] = sid
        meta["catName"] = cate["name"]
        yield scrapy.FormRequest(url = url,
            callback = self.readPage,
            formdata = data,
            meta = meta,
            dont_filter = True,
            errback = lambda x: self.download_errback(x, url)
        )

    def download_errback(self, e, url):
        print "=====error download -> try again========"
        city = listCity[self.indexCity]
        return scrapy.Request('https://vinalo.com/', 
                                cookies = {"tpvnl":city['sid']}, 
                                callback=self.readEachProvince,
                                meta = {"cityId":city['id'],"cityName":city["name"]},
                                dont_filter = True
                )

    def readPage(self, response):

        data = response.body.split("<cord>")
        data = filter(None, data) 
        meta = response.meta
        meta["last_item"] = False
        meta.pop('next_page', None)
        
        if len(data) <= 0:
            meta["last_item"] = True
            yield self.checkNextPage(meta)

        for i,d in enumerate(data):
            if i == len(data) -1:
                meta["last_item"] = True

            if d != "":
                if d.find('<viewkq>') >= 0:
                    s = d.split('<viewkq>')
                    d = s[0]
                    hxs = Selector(text=response.body)
                    nextPage = hxs.css('div.dcontain::attr(id)').extract()
                    print nextPage
                    if len(nextPage) > 0:
                        meta["next_page"] = nextPage[0]

                item = Host()
                item.parse(d)
                meta["item"] = d
                link = 'https://vinalo.com/%s-%s'%(item.alias,item.suffixId)
                # print link
                yield scrapy.Request(url=link, 
                        callback=self.readDetailHost,
                        meta = meta
                    )

        

        #next page
        if "next_page" in meta:
            nextPage = meta["next_page"]
            print('========next page=========')
            data = meta["data"]
            data["of"] = nextPage
            #load more
            yield scrapy.FormRequest(url = 'https://vinalo.com/loadh/morekqloai',
                    callback = self.readPage,
                    formdata = data,
                    meta = meta,
                    dont_filter = True,
                    errback = lambda x: self.download_errback(x, 'https://vinalo.com/loadh/morekqloai')
                )

    def readDetailHost(self, response):
        meta = response.meta
        str = meta["item"]
        item = Host()
        item.parse(str)

        print "===https://vinalo.com/%s-%s" % (item.alias,item.crawler)

        yield self.checkNextPage(meta)

        if item.checkExisted():
            # print "=========== existed host ================"
            # print "https://vinalo.com/%s-%s" % (item.alias,item.crawler)
            return

        yield {'image_urls':[item.image_profile]}
        image_guid = hashlib.sha1(item.image_profile).hexdigest()
        item.image_profile = '%s.jpg' % (image_guid)

        item.parseContent(response)
        id = item.insertDB()
        if id > 0:
            cityName = meta["cityName"]
            self.state[cityName] = self.state.get(cityName, 0) + 1
            # print "=========== new host ================"
            # print "https://vinalo.com/%s-%s" % (item.alias,item.crawler)

            #store tag
            objectTag = ObjectTag()
            for tagId in item.listTagId:
                if tagId > 0:
                    # print id, tagId
                    objectTag.insertNewObjectTag(id, tagId)

    def checkNextPage(self, meta):
        if "next_page" not in meta and "last_item" in meta and meta["last_item"] == True:
            self.indexSId += 1
            cate = listCate[self.indexListCate]
            city = listCity[self.indexCity]
            if self.indexSId < len(cate["sid"]):
                print "next sid"
                return scrapy.Request('https://vinalo.com/', 
                                cookies = {"tpvnl":city['sid']}, 
                                callback=self.readEachProvince,
                                meta = {"cityId":city['id'],"cityName":city["name"]},
                                dont_filter = True
                )

            self.indexSId = 0
            self.indexListCate += 1
            if self.indexListCate < len(listCate):
                print "next cate"
                return scrapy.Request('https://vinalo.com/', 
                                cookies = {"tpvnl":city['sid']}, 
                                callback=self.readEachProvince,
                                meta = {"cityId":city['id'],"cityName":city["name"]},
                                dont_filter = True
                )

            self.indexListCate = 0
            self.indexCity += 1
            city = listCity[self.indexCity]
            if self.indexCity < len(listCity):
                with open("stats", "w") as f:
                    for cityName,number in self.state.iteritems():
                        str = "%s: %s\n" % (slugify(cityName), number)
                        f.write(str)
                print "next city", slugify(city["name"])
                return scrapy.Request('https://vinalo.com/', 
                                cookies = {"tpvnl":city['sid']}, 
                                callback=self.readEachProvince,
                                meta = {"cityId":city['id'],"cityName":city["name"]},
                                dont_filter = True
                )
            





