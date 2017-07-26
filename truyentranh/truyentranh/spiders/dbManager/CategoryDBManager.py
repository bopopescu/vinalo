# -*- coding: utf-8 -*-

from BaseDBManager import BaseDBManager
from ..model.Category import Category
from ..model.Libs import *

class CategoryDBManager(BaseDBManager):
  table = "Category"
  typeClass = Category

  def addNewCategory(self, cate, site):
    item = self.fetchRow(cate, {"category_name": cate.category_name, "category_site":site})
    # print item
    '''add new category'''
    if item == None:
      cate.category_slug = makeAlias(cate.category_name)
      cate.category_site = site
      return self.insert(cate)
    return item['category_id']

if __name__ == '__main__':
  db = CategoryDBManager()
  cate = Category()
  cate.name = "haha"
  print db.addNewCategory(cate, "dammetruyen")
