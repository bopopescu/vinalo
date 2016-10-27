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

class UpdateKeywordSpider(scrapy.Spider):
    name = "updatekeyword"
    allowed_domains = ["vinalo.com"]

    def start_requests(self):
        host = Host()
        idx = 0
        limit = 10
        rows = host.getListHost(idx,limit)
        while len(rows) > 0:
            for row in rows:
                yield scrapy.Request('https://vinalo.com/%s-%s'%(row[1],row[2]),
                            callback = self.keyword,
                            dont_filter = True,
                            meta = {'id': row[0], 'tag': row[3], 'data': row}
                )
            idx += limit
            rows = host.getListHost(idx,limit)
        
    def keyword(self, response):
        meta = response.meta
        host = Host()
        print '============================='
        print meta['data']
        host.getKeyword(response)