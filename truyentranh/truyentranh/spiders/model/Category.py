# -*- coding: utf-8 -*-

from BaseModel import BaseModel

class Category(BaseModel):
  category_id = ""
  category_name = ""
  category_slug = ""
  category_site = ""

  __primaryKeys__ = ["category_id"]
  