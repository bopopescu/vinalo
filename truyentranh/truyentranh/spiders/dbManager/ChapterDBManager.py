# -*- coding: utf-8 -*-

from BaseDBManager import BaseDBManager
from ..model.Chapter import Chapter
from ..model.Libs import *

class ChapterDBManager(BaseDBManager):
  table = "Chapter"
  typeClass = Chapter

  def addNewChapter(self, chapter):
    item = self.fetchRow(chapter, 
                          {"chapter_name": chapter.chapter_name, 
                          "chapter_book":chapter.chapter_book}
    )
    # print item
    '''add new chapter'''
    if item == None:
      chapter.chapter_slug = makeAlias(chapter.chapter_name)
      return self.insert(chapter)
    return item['chapter_id']
    

