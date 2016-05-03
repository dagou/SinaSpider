# -*- coding: utf-8 -*-
import pymongo
from items import InformationItem, TweetsItem
import json
import MySQLdb
import settings
import sys
from scrapy import log

class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Sina"]
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Follows = db["Follows"]
        self.Fans = db["Fans"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, InformationItem):
            try:
                self.Information.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, TweetsItem):
            try:
                self.Tweets.insert(dict(item))
            except Exception:
                pass
        return item

class ScrapyWeiboPipeline(object):
    def __init__(self):
        try:
            self.db = MySQLdb.connect(settings.MYSQL_HOST, settings.USER_NAME, settings.PASSWORD, settings.DATABASE,
                                      charset="utf8")
            self.cursor = self.db.cursor()
        except MySQLdb.Error, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "File \"%s\", line %s. \n MySQL Error:%s" % (exc_traceback.tb_frame.f_code.co_filename,
                                                               exc_traceback.tb_lineno, e)

    def __del__(self):
        try:
            info = "close database."
            self.db.close()
        except (AttributeError, MySQLdb.Error), e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            info =  "Cound not destrut the ScrapWeiboPipeline.Object.\nFile \"%s\", line %s.\n MySql Error:%s" \
                  % (exc_traceback.tb_frame.f_code.co_filename, exc_traceback.tb_lineno, e)


    def process_item(self, item, spider):
        if isinstance(item, InformationItem):
            try:
                self._insertUserItem(item)
            except Exception:
                pass
        elif isinstance(item, TweetsItem):
            try:
                self._insertWeiboItem(item)
            except Exception:
                pass
        return item

    def _insertUserItem(self,item):
        uname = item['NickName'].encode("utf-8")

        sql = u"INSERT INTO sina.user(uid, uname, gender,province,city,signature,birthday, num_tweets,num_follows,num_fans,sex_orientation,marriage,url) " \
              u"VALUES(%s, %s, %s, %s,%s,%s, %s, %s, %s,%s,%s, %s, %s)"
        try:
            self.cursor.execute(sql, (item['_id'], item['NickName'], item['Gender'],
                                      item['Province'], item['City'], item['Signature'], item['Birthday'], item['Num_Tweets'],
                                      item['Num_Follows'], item['Num_Fans'], item['Sex_Orientation'], item['Marriage'], item['URL']))
            self.db.commit()
        except (AttributeError, MySQLdb.Error), e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "File \"%s\", line %s.\n MySql Error:%s" % (exc_traceback.tb_frame.f_code.co_filename,
                                                              exc_traceback.tb_lineno, e)
            log.ERROR("insert user Item error!!")
    def _insertWeiboItem(self, item):
        """
        Insert a WeiboItem into table in database
        :param item: WeiboItem
        :return: None
        """

        content = item['Content'].encode("utf-8")
        sql = u"INSERT INTO sina.feed(uid_weibo_id, uid, content, pubtime, co_oridinates, tools, zan, comments, transfers) " \
              u"VALUES(%s, %s, %s, %s,%s,%s, %s, %s, %s)"
        try:
            self.cursor.execute(sql, (item['_id'],item['ID'], content, item['PubTime'], item['Co_oridinates'],
                                      item['Tools'],item['Like'],item['Comment'],item['Transfer']))
            self.db.commit()
        except (AttributeError, MySQLdb.Error), e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "File \"%s\", line %s.\n MySql Error:%s" % (exc_traceback.tb_frame.f_code.co_filename,
                                                              exc_traceback.tb_lineno, e)
            log.ERROR("insert WeiboItem  error!!")

