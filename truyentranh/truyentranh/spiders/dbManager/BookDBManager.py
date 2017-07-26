# -*- coding: utf-8 -*-

from BaseDBManager import BaseDBManager
from ..model.Book import Book
from ..model.Chapter import Chapter
from ..model.Libs import *

class BookDBManager(BaseDBManager):
  table = "Book"
  typeClass = Book
  
  def addNewBook(self, book, site = 0):
    item = self.fetchRow(book, {"book_name": book.book_name, "book_site":site})
    # print item
    '''add new category'''
    if item == None:
      book.book_site = site
      book.book_slug = makeAlias(book.book_name)
      return self.insert(book)
    return item['book_id']

  def updateBook(self, obj, data, where = {}):
    """ Don't have specific where """
    if not where:
      primaryKeys = {k:getattr(obj,k) for k in self.typeClass.__primaryKeys__}
      return self.update(data, primaryKeys)

    ''' Has specific where '''  
    return self.update(data, where)

if __name__ == '__main__':
  db = BookDBManager()
  book = Book()
  book.name = "alidiep"
  book.author = "fuck"
  # print db.addNewBook(book)
  print db.updateBook({"name":"alidiep","author":"fuck"}, {"id":12,"fuck":"hhaa"})
