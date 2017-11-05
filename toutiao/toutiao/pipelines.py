# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql,pymysql.cursors
from twisted.enterprise import adbapi


class ToutiaoPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipline(object):
#异步机制写入数据库
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
        host=settings['MYSQL_HOST'],
        db=settings['MYSQL_DBNAME'],
        user=settings['MYSQL_USER'],
        passwd=settings['MYSQL_PASSWORD'],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
        use_unicode=True,
        )

        dbpool=adbapi.ConnectionPool('pymysql',**dbparms)
        return cls(dbpool)
    def process_item(self,item,spider):
        #twisted异步插入MySQL
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)#处理异常

    def handle_error(self,failure,item,spider):
        print(failure)

    def do_insert(self,cursor,item):
        #执行插入,根据不同item构建语句
        insert_sql,params=item.get_insert_sql()

        cursor.execute(insert_sql,params)