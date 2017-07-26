# -*- coding: utf-8 -*-
import scrapy
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
from model.Libs import *
from model.Book import Book
from dbManager.BookDBManager import BookDBManager

class DammetruyenSpider(scrapy.Spider):
  name = "dammetruyen"
  allowed_domains = ["dammetruyen.com"]
  
  site = 1 #dammetruyen
  bookDBManager = BookDBManager()

  def start_requests(self):
    # self.crawler.engine.slot.scheduler.df.fingerprints = set()

    yield scrapy.Request('http://dammetruyen.com',
          callback=self.readListCategory
    )

  def readListCategory(self, response):
    soup = BeautifulSoup(response.body,'lxml')
    menu = soup.findAll('li', {'id' : 'menu-item-92'})
    # logging.log(logging.WARNING, "Count: %d", len(listItems))
    for item in menu:
      a = item.find('a')
      # print a.text.encode('utf-8', 'ignore'), a.get('href')
      yield scrapy.Request(a.get('href'),
          callback=self.readEachCategory
      )
      break

  def readEachCategory(self, response):
    soup = BeautifulSoup(response.body,'lxml')
    listBook = soup.findAll('div', {'class' : 'manga_list'})
    for bookEle in listBook:
      listA = bookEle.findAll('a')
      
      book = Book()
      book.book_name = listA[0].get('title').encode('utf-8')
      book.book_site = self.site

      book.book_id = self.bookDBManager.addNewBook(book)
      yield scrapy.Request(listA[0].get('href'),
          callback=self.readDetailBook,
          meta={'book': book}
      )
      break

  def readDetailBook(self, response):
    book = response.meta['book']
    soup = BeautifulSoup(response.body,'lxml')
    listDetail = soup.findAll('div', {'class' : 'det'})
    listP = listDetail[0].findAll('p')

    data = {}

    '''description'''
    data['book_description'] = listP[1].text.encode('utf-8')
    # print book.book_description

    '''author'''
    txtAuthor = listP[5].text.encode('utf-8')
    data['book_author'] = txtAuthor.split(':')[1].strip()
    # print book.book_author

    self.bookDBManager.updateBook(book, data)

