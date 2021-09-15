# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BilidemoItem(scrapy.Item):
    # define the fields for your item here like:
    v_name = scrapy.Field()
    v_uid=scrapy.Field()
    ctime=scrapy.Field()
    dyn_out=scrapy.Field()
    oid_out=scrapy.Field()
    type_out=scrapy.Field()
    acount=scrapy.Field()
    count=scrapy.Field()
    # pass

class replyItem(scrapy.Item):
    table_name=scrapy.Field()
    r_uid = scrapy.Field()
    r_name = scrapy.Field()
    comment = scrapy.Field()
    c_time = scrapy.Field()
    dynamic = scrapy.Field()
    r_type= scrapy.Field()
    replies=scrapy.Field()
    rpid=scrapy.Field()

class douchuItem(scrapy.Item):
    title=scrapy.Field()
    author = scrapy.Field()
    replies = scrapy.Field()
    e_time = scrapy.Field()
    url=scrapy.Field()