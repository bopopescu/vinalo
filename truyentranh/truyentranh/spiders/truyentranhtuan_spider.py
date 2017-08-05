# -*- coding: utf-8 -*-
import scrapy
import sys
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json
from scrapy.http import FormRequest
import pprint
import urllib
from lxml.html import HTMLParser, fromstring
from scrapy.selector import Selector
from datetime import datetime
from slugify import slugify
from bs4 import BeautifulSoup
import logging
import re
from model.Libs import *
from model.Book import Book
from model.Chapter import Chapter
from model.Category import Category
from dbManager.BookDBManager import BookDBManager
from dbManager.ChapterDBManager import ChapterDBManager
from dbManager.CategoryDBManager import CategoryDBManager
from dbManager.MapBookCategoryDBManager import MapBookCategoryDBManager

class TruyenTranhTuanSpider(scrapy.Spider):
  name = "truyentranhtuan"
  allowed_domains = ["truyentranhtuan.com"]
  
  site = 1 #dammetruyen
  bookDBManager = BookDBManager()
  chapterDBManager = ChapterDBManager()
  mapBookCategoryDBManager = MapBookCategoryDBManager()
  dbCategory = CategoryDBManager()

  def start_requests(self):
    # self.crawler.engine.slot.scheduler.df.fingerprints = set()

    yield scrapy.Request('http://truyentranhtuan.com/danh-sach-truyen',
          callback=self.readPage
    )

  def readPage(self, response):
    soup = BeautifulSoup(response.body,'lxml')
    menu = soup.findAll('div', {'class' : 'manga-focus'})
    
    for item in menu:
      a = item.findAll('a')[0]
      # print a.text.encode('utf-8', 'ignore').strip(), a.get('href').strip()
      book = Book()
      book.book_name = a.text.encode('utf-8', 'ignore').strip()
      link = a.get('href').strip()
      yield scrapy.Request(link,
          callback=self.readDetail,
          meta = {'book': book}
      )

      """debug"""
      # break
  
  def getText(self, ele):
    if ele != None:
      return ele.text.encode('utf-8', 'ignore').strip()
    return ""

  def readDetail(self, response):
    soup = BeautifulSoup(response.body,'lxml')
    book = response.meta['book']
    
    p = soup.findAll('p', {'class': 'misc-infor'})
    '''author'''
    book.book_author = self.getText(p[1].find('a'))

    '''category'''
    book_category = []
    listCates = p[2].findAll('a')
    for cate in listCates:
      category = Category()
      category.category_name = cate.text.encode('utf-8', 'ignore').strip()
      book_category.append(self.dbCategory.addNewCategory(category, self.site))
    # print book_category

    '''description'''
    div = soup.find('div', {'id':'manga-summary'})
    book.book_description = self.getText(div)

    book.book_id = self.bookDBManager.addNewBook(book, self.site)

    self.mapBookCategoryDBManager.addBookCategory(book, book_category)

    '''chapter'''
    listChapter = soup.findAll('span', {'class': 'chapter-name'})
    order = len(listChapter)
    for ele in listChapter:
      chapter = Chapter()
      chapter.chapter_book = book.book_id
      chapter.chapter_name = self.getText(ele)
      chapter.chapter_order = order
      order -= 1
      a = ele.find('a')
      yield scrapy.Request(a.get('href').strip(),
          callback=self.readContentChapter,
          meta = {'chapter': chapter}
      )

      """debug"""
      # break

  def readContentChapter(self, response):
    soup = BeautifulSoup(response.body,'lxml')
    chapter = response.meta['chapter']
    # print response.url, response.body
    m = re.search('slides_page_url_path\s+=\s+(.+?);', response.body)
    if m:
      found = m.group(1)
      chapter.chapter_content = found

    self.chapterDBManager.addNewChapter(chapter)  
