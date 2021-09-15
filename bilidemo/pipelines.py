# -*- coding: utf-8 -*-
from scrapy.exporters import  CsvItemExporter
import json
from collections import OrderedDict
import pymysql
from .items import BilidemoItem,replyItem,douchuItem
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BilidemoPipeline:
    def process_item(self, item, spider):
        # item = OrderedDict(item)
        # item = json.dumps(item, ensure_ascii=False)
        return item
        # pass

# 保存到数据库
class MySQLPipeline:
    def __init__(self,host,port,user,password,database):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASS'),
            database=crawler.settings.get('MYSQL_DATABASE'),
        )

    def open_spider(self,spider):
        self.dyn_connent=pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset='utf8mb4')
        self.dyn_cursor=self.dyn_connent.cursor()
        self.rep_connent = pymysql.connect(host=self.host, user=self.user, password=self.password, database='bili_replies',charset='utf8mb4')
        self.rep_cursor=self.rep_connent.cursor()
        self.douchu_connent = pymysql.connect(host=self.host, user=self.user, password=self.password, database='douchu',charset='utf8mb4')
        self.douchu_cursor=self.douchu_connent.cursor()
    def close_spider(self,spider):
        self.dyn_connent.close()
        self.rep_cursor.close()

    def process_item(self,item,spider):
        if isinstance(item, BilidemoItem):
            # print('type1')
#             SQL_create = f"""
#             CREATE TABLE IF NOT EXISTS v_{item['v_uid']}_dynamic (
# --             id BIGINT auto_increment PRIMARY KEY,
#             v_uid BIGINT NOT NULL ,
#             v_name TEXT NOT NULL ,
#             ctime Datetime NOT NULL,
#             dynamic BIGINT NOT NULL,
#             oid BIGINT NOT NULL,
#             type BIGINT NOT NULL,
#             acount BIGINT NOT NULL,
#             count BIGINT NOT NULL
#             )ENGINE=innodb DEFAULT CHARSET=utf8mb4;
#             """
            SQL_write= f"INSERT INTO v_{item['v_uid']}_dynamic(v_uid,v_name,ctime,dynamic,oid,type,acount,count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            # print('**************************')
            # self.dyn_cursor.execute(SQL_create)
            self.dyn_cursor.execute(SQL_write, [item['v_uid'], item['v_name'], item['ctime'], item['dyn_out'], item['oid_out'], item['type_out'], item['acount'], item['count']])
            self.dyn_connent.commit()

        if isinstance(item, replyItem):
            # print('type2')
            # print('rw',end='')
#             SQL_create = f"""
#             CREATE TABLE IF NOT EXISTS r_{item['table_name']}_replies (
# --             id BIGINT auto_increment PRIMARY KEY,
#             r_uid BIGINT NOT NULL ,
#             r_name TEXT NOT NULL ,
#             c_time Datetime NOT NULL,
#             comment TEXT NOT NULL,
#             dynamic BIGINT NOT NULL,
#             r_type TEXT NOT NULL,
#             replies BIGINT NOT NULL,
#             rpid BIGINT NOT NULL
#             )ENGINE=innodb DEFAULT CHARSET=utf8mb4;
#             """
            SQL_write= f"INSERT INTO r_{item['table_name']}_replies(r_uid,r_name,c_time,comment,dynamic,r_type,replies,rpid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            self.rep_cursor.execute(SQL_write, [item['r_uid'], item['r_name'], item['c_time'], item['comment'], item['dynamic'], item['r_type'],item['replies'],item['rpid']])
            self.rep_connent.commit()

        if isinstance(item, douchuItem):
            SQL_create = f"""
                        CREATE TABLE IF NOT EXISTS douchu_ties (
                        id BIGINT auto_increment PRIMARY KEY,
                        title TEXT NOT NULL ,
                        author TEXT NOT NULL ,
                        replies INT NOT NULL,
                        e_time TEXT NOT NULL,
                        url TEXT NOT NULL
                        )ENGINE=innodb DEFAULT CHARSET=utf8mb4;
                        """
            SQL_write = f"INSERT INTO douchu_ties(title,author,replies,e_time,url) VALUES (%s,%s,%s,%s,%s)"
            self.douchu_cursor.execute(SQL_create)
            self.douchu_cursor.execute(SQL_write,[item['title'], item['author'], item['replies'], item['e_time'], item['url']])
            self.douchu_connent.commit()
        return item


