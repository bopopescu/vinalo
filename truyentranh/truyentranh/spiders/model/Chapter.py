# -*- coding: utf-8 -*-

from BaseModel import BaseModel

class Chapter(BaseModel):
  chapter_id = ""
  chapter_book = ""
  chapter_name = ""
  chapter_slug = ""
  chapter_order = ""
  chapter_content = ""

  __primaryKeys__ = ["chapter_id"]

  