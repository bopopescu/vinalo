# -*- coding: utf-8 -*-

from BaseDBManager import BaseDBManager
from ..model.Category import Category
from ..model.Book import Book
from ..model.MapBookCategory import MapBookCategory
from ..model.Libs import *

class MapBookCategoryDBManager(BaseDBManager):
  table = "map_book_category"
  typeClass = MapBookCategory

  def addBookCategory(self, book, listCate):
    mapBookCategory = MapBookCategory()
    mapBookCategory.book_id = book.book_id
    for idCate in listCate:
      mapBookCategory.category_id = idCate
      self.insert(mapBookCategory)
