# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest
from pyquery import PyQuery as pq
import json
from lxml.html import HTMLParser, fromstring
from scrapy.selector import Selector
from pprint import pprint
from model.city import City

class CitySpider(scrapy.Spider):
    name = 'city'
    start_urls = ['https://vinalo.com/loadh/allthpho']

    def start_requests(self):
        url = 'https://vinalo.com/loadh/allthpho'
        data = {
            "img": "60078596",
        }
        return [FormRequest(url = url, 
                callback = self.parse,
                formdata = data
            )]

    def parse(self, response):

        hxs = Selector(text=response.body)
        desc = hxs.xpath('//div[@class="divaczfp"]').extract()

        res = []
        a = "["
        city = City()
        for item in desc:
            html = Selector(text=item)
            arrName = html.xpath('//@val').extract()[0].encode('utf-8').split('-')
            cityName = html.xpath('//p[@class="pacz_2"]/text()').extract()[0].encode('utf-8')
            if item != desc[0]:
                a += ","
            id = city.getIdCityFromName(cityName)
            print(id)
            a += '{"name":"%s","sid":"%s","id":"%s"}' %(cityName,arrName[0],id)

        a += "]"
        with open('city', 'w') as file:
            # file.write(json.dumps(res, encoding="utf-8"))
            file.write(a)

        # with open('city') as file:
        #     res = json.load(file)
        #     print(res[1]['name'])