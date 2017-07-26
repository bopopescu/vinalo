# -*- coding: utf-8 -*-

from BaseDBManager import BaseDBManager
from ..model.Chapter import Chapter
from ..model.Libs import *

class ChapterDBManager(BaseDBManager):
  table = "Chapter"
  typeClass = Chapter

  def addNewChapter(self, chapter):
    chapter.chapter_slug = makeAlias(chapter.chapter_name)
    return self.insert(chapter)

