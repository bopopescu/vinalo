# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline, ImageException
from scrapy.http import Request
from cStringIO import StringIO
import hashlib

class TruyentranhPipeline(ImagesPipeline):
  def get_media_requests(self, item, info):
    for image_url in item['image_urls']:
      yield Request(image_url)
      
  def item_completed(self, results, item, info):
    item['images'] = [x for ok, x in results if ok]
    return item
 
  def file_path(self, request, response=None, info=None):
    image_guid = hashlib.sha1(request.url).hexdigest()
    return '%s.jpg' % (image_guid)
