# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import FormRequest
from model.host import Host
import pprint
import urllib
from lxml.html import HTMLParser, fromstring
from scrapy.selector import Selector
from datetime import datetime
from model.city import City

with open("city") as file:
    listCity = json.load(file)

with open('category') as file:
    listCate = json.load(file)

class VinaloSpider(scrapy.Spider):
    name = "vinalo"
    allowed_domains = ["vinalo.com"]
    start_urls = (
        'https://vinalo.com/loadh/getddloai',
    )
    firstPage = True
    loadMore = 'https://vinalo.com/loadh/morekqloai'
    cateId = "52552f0af525bc126c92e5a5"

    def start_requests(self):
        for city in listCity:
            # print "city ", city["name"]
            yield scrapy.Request('https://vinalo.com', 
                cookies = {"tpvnl":city['sid']}, 
                callback=self.readEachProvice,
                meta = {"cityId":city['id'],"cityName":city["name"]}
            )
            # break

    def readEachProvice(self, response):
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
        for cate in listCate:
            for i,sid in enumerate(cate["sid"]):
                if i < len(cate['lddc']):
                    data['lddc'] = cate['lddc'][i]
                data['ldd'] = sid
                meta["data"] = data
                meta["typeId"] = cate["id"]
                meta["sid"] = sid
                # print "category ", cate["name"], " ", sid
                #first page
                yield scrapy.FormRequest(url = url,
                    callback = self.readPage,
                    formdata = data,
                    meta = meta
                )
                # break
            # break


    def readPage(self, response):
        data = response.body.split("<cord>")
        # with open('html', 'wb') as file:
        #     file.write(response.body)
        meta = response.meta
        for d in data:
            item = Host()
            item.parse(d)
            meta["item"] = d
            # print(item.name)
            # print('https://vinalo.com/%s-%s'%(item.alias,item.suffixId))
            yield scrapy.Request(url='https://vinalo.com/%s-%s'%(item.alias,item.suffixId), 
                    callback=self.readDetailHost,
                    meta = meta
                    )
            # break
        # return
        #get nextpage
        hxs = Selector(text=response.body)
        nextPage = hxs.css('div.dcontain::attr(id)').extract()
        if len(nextPage) > 0:
            nextPage = nextPage[0]
            # print('========next page=========')
            data = meta["data"]
            data["of"] = nextPage
            #load more
            yield scrapy.FormRequest(url = 'https://vinalo.com/loadh/morekqloai',
                    callback = self.readPage,
                    formdata = data,
                    meta = meta
                )

    def readDetailHost(self, response):
        str = response.meta["item"]
        item = Host()
        item.parse(str)

        if item.checkExisted():
            # print "=========== existed host ================"
            return

        item.parseContent(response)
        id = item.insertDB()
        if id > 0:
            cityName = response.meta["cityName"]
            self.state[cityName] = self.state.get(cityName, 0) + 1







