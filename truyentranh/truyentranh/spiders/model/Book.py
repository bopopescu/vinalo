# -*- coding: utf-8 -*-

from BaseModel import BaseModel

class Book(BaseModel):
  book_id = ""
  book_name = ""
  book_author = ""
  book_slug = ""
  book_linkUpdate = ""
  book_site = ""
  book_description = ""
  book_otherName = ""

  __primaryKeys__ = ["book_id"]
  