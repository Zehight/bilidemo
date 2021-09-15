# -*- coding: utf-8 -*-
import scrapy
import pymysql
import math
import time
import json
from ..items import BilidemoItem, replyItem


class BiliLzlSpider(scrapy.Spider):
    name = 'bili_lzl'
    allowed_domains = ['api.vc.bilibili.com']
    # log-长度记录
    total_len = 0
    now_len_bz= 0
    # log-时间记录
    t1 = time.time()
    start_time = t1
    # url列表
    s_u = []
    def __init__(self,v_uids='', *args,**kwargs):
        super().__init__(*args, **kwargs)
        v_uids = eval(v_uids)
        gets = ()
        lzl_connent = pymysql.connect(host='localhost', user='root', password='000000', database='bili_replies',
                                      charset='utf8mb4')
        lzl_cursor = lzl_connent.cursor()
        for v_uid in v_uids:
            sql = f'''
            SELECT
                bili_dynamic.v_{v_uid}_dynamic.v_uid, 
                bili_replies.r_{v_uid}_replies.dynamic, 
                bili_replies.r_{v_uid}_replies.replies, 
                bili_dynamic.v_{v_uid}_dynamic.oid, 
                bili_dynamic.v_{v_uid}_dynamic.type, 
                bili_replies.r_{v_uid}_replies.rpid
            FROM
                bili_replies.r_{v_uid}_replies,
                bili_dynamic.v_{v_uid}_dynamic
            WHERE
                bili_replies.r_{v_uid}_replies.dynamic = bili_dynamic.v_{v_uid}_dynamic.dynamic AND
                bili_replies.r_{v_uid}_replies.replies > 2
            '''
            lzl_cursor.execute(sql)
            gets=gets+lzl_cursor.fetchall()
        lzl_connent.close()
        for get in gets:
            page = math.ceil(get[2] / 20) + 1
            for i in range(1, page):
                self.s_u.append(
                    [f'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={i}&type={get[4]}&oid={get[3]}&ps=20&root={get[5]}',
                     get[0], get[1]])
        self.total_len = len(self.s_u)

    def start_requests(self):
        # 把所有的URL地址统一扔给调度器入队列
        for strat_url in self.s_u:
            # 交给调度器
            yield scrapy.Request(
                url=strat_url[0],
                meta={'table_name':strat_url[1],'dynamic_id':strat_url[2]},
                callback=self.parse
            )

    def parse(self, response):
        self.now_len_bz = (self.now_len_bz + 1)
        avg_time=round((time.time() - self.start_time) / self.now_len_bz,2)
        pre_time=round((self.total_len-self.now_len_bz)*avg_time,2)
        ben_time=round(time.time()-self.t1,2)
        print('[完/总', self.now_len_bz, '/', self.total_len, end=']')
        print('[进度: {:.2%}'.format(self.now_len_bz / self.total_len), end=']')
        print(f'[本次时间：{ben_time}', end=']')
        print(f'[平均时间：{avg_time}',end=']')
        print(f'[平均并发：{round(1/avg_time,2)}', end=']')
        print(f'[剩余{round(pre_time/3600,2)}小时完成',end=']')
        print(f'[正在请求：{len(self.crawler.engine.slot.inprogress)}正在队列：{len(self.crawler.engine.slot.scheduler)}]')
        self.t1 = time.time()
        try:
            test = json.loads(response.text)['data']['replies'][0]['member']['uname']
        except:
            return
        table_name=response.meta['table_name']
        dynamic_id=response.meta['dynamic_id']
        reply_list=json.loads(response.text)['data']['replies']
        for reply in reply_list:
            r_item=replyItem()
            r_item['table_name']=table_name
            r_item['r_uid'] = reply['member']['mid']
            r_item['r_name'] = reply['member']['uname']
            r_item['comment'] = reply['content']['message']
            r_item['c_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(reply['ctime']))
            r_item['dynamic'] = dynamic_id
            r_item['r_type'] = '楼中楼'
            r_item['replies'] = 0
            r_item['rpid'] = reply['root']
            yield r_item
