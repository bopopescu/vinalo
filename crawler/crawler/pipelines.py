# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline, ImageException
from scrapy.http import Request
from cStringIO import StringIO
import hashlib

class MyImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x) for x in item.get('image_urls', [])]   
        
    def item_completed(self, results, item, info):
        item['images'] = [x for ok, x in results if ok]
        return item
   
    def image_key(self, url):
        image_guid = hashlib.sha1(url).hexdigest()
        return '%s.jpg' % (image_guid)   
