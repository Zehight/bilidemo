# -*- coding: utf-8 -*-
import os
import time
import pymysql

start=time.time()
print(f'开始爬取')
uids = '[703007996,672346917,672353429,672342685,351609538]'
# uids = '[672328094]'
v_uids=uids

def jianku(v_uids):
    v_uids=eval(v_uids)
    lzl_connent_wn = pymysql.connect(host='localhost', user='root', password='000000', database='bili_dynamic',
                                     charset='utf8mb4')
    lzl_connent = pymysql.connect(host='localhost', user='root', password='000000', database='bili_replies',
                                  charset='utf8mb4')
    lzl_cursor = lzl_connent.cursor()
    lzl_cursor_wn = lzl_connent_wn.cursor()
    for v_uid in v_uids:
        SQL_create_dy = f"""
                    CREATE TABLE IF NOT EXISTS v_{v_uid}_dynamic (
        --             id BIGINT auto_increment PRIMARY KEY,
                    v_uid BIGINT NOT NULL ,
                    v_name TEXT NOT NULL ,
                    ctime Datetime NOT NULL,
                    dynamic BIGINT NOT NULL,
                    oid BIGINT NOT NULL,
                    type BIGINT NOT NULL,
                    acount BIGINT NOT NULL,
                    count BIGINT NOT NULL
                    )ENGINE=innodb DEFAULT CHARSET=utf8mb4;
                    """
        SQL_create = f"""
                    CREATE TABLE IF NOT EXISTS r_{v_uid}_replies (
        --             id BIGINT auto_increment PRIMARY KEY,
                    r_uid BIGINT NOT NULL ,
                    r_name TEXT NOT NULL ,
                    c_time Datetime NOT NULL,
                    comment TEXT NOT NULL,
                    dynamic BIGINT NOT NULL,
                    r_type TEXT NOT NULL,
                    replies BIGINT NOT NULL,
                    rpid BIGINT NOT NULL
                    )ENGINE=innodb DEFAULT CHARSET=utf8mb4;
                    """
        lzl_cursor_wn.execute(SQL_create_dy)
        lzl_cursor.execute(SQL_create)
    lzl_connent.commit()
    lzl_connent_wn.commit()
    lzl_connent_wn.close()
    lzl_connent.commit()
    lzl_connent.close()

jianku(v_uids)

#
os.system(f"scrapy crawl bili_dynamic -a uids={uids} --nolog")
end1=time.time()
print(f'****************以收集完成所有动态数据，耗时{end1-start}秒********************')
os.system(f"scrapy crawl bili_replies -a v_uids={v_uids} --nolog")
end2=time.time()
print(f'****************以收集完成所有楼层数据，耗时{end2-start}秒********************')
os.system(f"scrapy crawl bili_lzl -a v_uids={v_uids} --nolog")
end=time.time()
print(f'楼中楼数据全部采集完毕，一共花费{end-start}秒，{(end-start)/60}分钟')