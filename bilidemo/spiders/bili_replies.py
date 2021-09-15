# -*- coding: utf-8 -*-
import scrapy
import pymysql
import math
import time
import json
from ..items import BilidemoItem,replyItem

class BiliRepliesSpider(scrapy.Spider):
    name = 'bili_replies'
    allowed_domains = ['api.vc.bilibili.com']
    # log-长度记录
    total_len = 0
    now_len_bz= 0
    # log-时间记录
    t1 = time.time()
    start_time = t1
    now_time = 0
    s_u=[]
    def __init__(self,v_uids='', *args,**kwargs):
        super().__init__(*args, **kwargs)
        v_uids = eval(v_uids)
        gets = ()
        url_connent = pymysql.connect(host='localhost', user='root', password='000000', database='bili_dynamic',
                                      charset='utf8mb4')
        url_cursor = url_connent.cursor()
        print(v_uids,type(v_uids))
        for v_uid in v_uids:
            sql = f'''
            SELECT
            v_{v_uid}_dynamic.v_uid, 
            v_{v_uid}_dynamic.dynamic, 
            v_{v_uid}_dynamic.oid, 
            v_{v_uid}_dynamic.type, 
            v_{v_uid}_dynamic.count
            FROM
            v_{v_uid}_dynamic
            '''
            url_cursor.execute(sql)
            gets = gets + url_cursor.fetchall()
        url_connent.close()
        for get in gets:
            page = math.ceil(get[4] / 20) + 1
            for i in range(1, page):
                self.s_u.append(
                    [f'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={i}&type={get[3]}&oid={get[2]}&mode=3',
                     get[0], get[1]])
        self.total_len = len(self.s_u)

    def start_requests(self):
        for strat_url in self.s_u:
            url = strat_url
            # 交给调度器
            yield scrapy.Request(
                url=url[0],
                meta={'table_name':url[1],'dynamic_id':url[2]},
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
            r_item['r_type'] = '楼主'
            r_item['replies'] = reply['rcount']
            r_item['rpid'] = reply['rpid']
            try:
                lzl_replies=[reply['replies'][0],reply['replies'][1]]
                for lzl_reply in lzl_replies:
                    lzl_item = replyItem()
                    lzl_item['table_name'] = table_name
                    lzl_item['r_uid'] = lzl_reply['member']['mid']
                    lzl_item['r_name'] = lzl_reply['member']['uname']
                    lzl_item['comment'] = lzl_reply['content']['message']
                    lzl_item['c_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lzl_reply['ctime']))
                    lzl_item['dynamic'] = dynamic_id
                    lzl_item['r_type'] = '楼中楼'
                    lzl_item['replies'] = 0
                    lzl_item['rpid'] = lzl_reply['root']
                    yield lzl_item
            except:
                pass
            yield r_item