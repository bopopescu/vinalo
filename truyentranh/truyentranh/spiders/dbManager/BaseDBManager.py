# -*- coding: utf-8 -*-

from slugify import slugify
from ..model.db import MyDB
from ..model.libs import *
import logging

class BaseDBManager:
  db = MyDB()
  table = ""
  typeClass = object

  def insert(self, obj):
    self.db.query("set names utf8;", None)
    try:
      query = self.prepareInsert(obj)
      columns = self.exportColumn(obj)
      data = map(lambda x: getattr(obj,x), columns)
      # print query
      # print data
      # print tuple(data)
      self.db.query(query, tuple(data))
      self.db.commit()
      return self.db.getLastId()
    except UnicodeDecodeError as err:
      print "insert error: ", err
      print self.db._db_cur._executed
    return None

  def update(self, values, where):
    self.db.query("set names utf8;", None)
    try:
      query = self.prepareUpdate(values, where)
      data = self.exportValue(values)
      dataWhere = data.extend(self.exportValue(where))
      # print data
      # print query
      self.db.query(query, tuple(data))
      self.db.commit()
      return self.db.getLastId()
    except UnicodeDecodeError as err:
      print "insert error: ", err
      print self.db._db_cur._executed
    return None

  def fetchRow(self, obj, where):
    self.db.query("set names utf8;", None)
    try:
      query = self.prepareSelect(obj, [], where)
      query = "%s LIMIT 1" % query
      data = self.exportValue(where)
      # print data
      # print query
      res = self.db.fetchRow(query, tuple(data))
      return res[0] if len(res)>0 else None
    except UnicodeDecodeError as err:
      print "insert error: ", err
      print self.db._db_cur._executed
    return None

  def fetchAll(self, where):
    pass

  def attrs(self):
    #remove key __module__, __doc__, ...
    listAttr = {k: v for k, v in self.typeClass.__dict__.iteritems() if k.find("__")}
    return listAttr

  def prepareInsert(self, obj):
    listColumns = self.exportColumn(obj)
    column = ','.join(listColumns)
    val = ','.join("%s" for i in xrange(len(listColumns)))
    return "INSERT INTO %s (%s) VALUES (%s)" % (self.table,column,val)

  def prepareUpdate(self, values, where):
    allProperties = self.exportColumn()

    #Description: listPropertyUpdating = allProperties.join(values)
    listPropertyUpdating = {k:v for k, v in values.iteritems() if k in allProperties}
    txtSet = ','.join("%s=%%s"%k for k in listPropertyUpdating)

    if len(listPropertyUpdating) != len(values):
      DDLogDebug('Property miss match')

    #Description: listWhere = allProperties.join(where)
    listWhere = {k for k in where if k in allProperties}
    txtWhere = ' AND '.join("%s=%%s"%k for k in listWhere)

    if len(listWhere) != len(where):
      DDLogDebug('Property miss match')

    return "UPDATE %s SET %s WHERE %s" % (self.table,txtSet,txtWhere)

  def prepareSelect(self, obj, columns=[], where={}):
    allProperties = self.exportColumn()

    #Description: listPropertySelecting = allProperties.join(columns)
    listPropertySelecting = {k for k in columns if k in allProperties}
    txtSelect = "*"
    if len(listPropertySelecting) > 0:
      txtSelect = ','.join("%s=%%s"%k for k in listPropertyUpdating)

    if len(columns) > 0 and len(listPropertySelecting) != len(columns):
      DDLogDebug('Property miss match') 

    #Description: listWhere = allProperties.join(where)
    listWhere = {k:v for k, v in where.iteritems() if k in allProperties}
    txtWhere = ' AND '.join("%s=%%s"%k for k in listWhere)

    if len(listWhere) != len(where):
      DDLogDebug('Property miss match')

    return "SELECT %s FROM %s WHERE %s" % (txtSelect,self.table,txtWhere)

  def exportColumn(self,obj = None):
    listAttrs = self.attrs()

    if obj == None:
      return listAttrs.keys()

    if isinstance(obj, dict):
      listKey = {k:v for k, v in obj.iteritems() if k in listAttrs}
      return listKey.keys()
    elif isinstance(obj, list):
      listKey = {k for k in obj if k in listAttrs}
      return listKey
    else:
      listKey = {k for k in listAttrs if getattr(obj, k) != None and getattr(obj, k) != ""}
      return listKey

  def exportValue(self, obj):
    listAttrs = self.attrs()
    if isinstance(obj, dict):
      listValue = {k:v for k, v in obj.iteritems() if k in listAttrs}
      return listValue.values()
    elif isinstance(obj, list):
      listValue = {k for k in obj if k in listAttrs}
      return listValue
    else:
      listValue = {getattr(obj, k) for k in listAttrs if getattr(obj, k) != None and getattr(obj, k) != ""}
      return listValue

  def makeAlias(self,name):
    name = name.replace(u'đ', u'd')
    try:
      txt = slugify(name)
      return txt
    except UnicodeEncodeError as err:
      print err
      print name
    return ""


