# -*- coding: utf-8 -*-
# encoding=utf8

import inspect
import logging
from slugify import slugify
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

def writeFile(name, content):
  with open(name, 'wb') as f:
    f.write(content)

#Format: type:user_os:class:function:line:content
def DDLogDebug(content,level=logging.WARNING):
  stack = inspect.stack()
  the_class = stack[1][0].f_locals["self"].__class__
  the_method = stack[1][0].f_code.co_name
  caller = inspect.getframeinfo(stack[1][0])
  {
    logging.INFO: logging.info("%s:%s:%s"%(the_class,the_method,content)),
    logging.WARNING: logging.warning("%s:%s:%d:%s"%(the_class,the_method,caller.lineno,content)),
  }[level]

def makeAlias(name):
  name = name.replace(u'đ', u'd')
  try:
    txt = slugify(name)
    return txt
  except UnicodeEncodeError as err:
    print err
    print name
  return ""