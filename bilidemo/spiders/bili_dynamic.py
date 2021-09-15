# -*- coding: utf-8 -*-
import scrapy
import json
import time
from ..items import BilidemoItem,replyItem
import math
from tqdm import tqdm

# false = False
# true = True
# null = ''


class BiliDynamicSpider(scrapy.Spider):
    name = 'bili_dynamic'
    allowed_domains = ['api.vc.bilibili.com']
    # uids = [703007996,672346917,672353429,672342685,672328094,351609538]
    # uids=[672328094]
    def __init__(self, uids=None, *args, **kwargs):
        super(BiliDynamicSpider, self).__init__(*args, **kwargs)
        self.uids=eval(uids)
        print([f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}&offset_dynamic_id=0" for uid in self.uids])
        self.start_urls = [f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}&offset_dynamic_id=0" for uid in self.uids]

    total_len=0
    now_len=0
    url_count=0
    def parse(self, response):
        if json.loads(response.text)['data']['has_more']==0:
            return
        card_list = json.loads(response.text)['data']['cards']
        self.total_len=self.total_len+len(json.loads(response.text)['data']['cards'])
        for card in card_list:
            item = BilidemoItem() #实例化item
            item['v_name'] = card['desc']['user_profile']['info']['uname']
            item['v_uid'] = card['desc']['uid']
            item['ctime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(card['desc']['timestamp']))
            type_in = card['desc']['type']
            oid_in = card['desc']['rid']
            dyn_in = card['desc']['dynamic_id']
            if type_in == 8:
                item['dyn_out'] = dyn_in
                item['oid_out'] = oid_in
                item['type_out'] = 1
            elif type_in == 2:
                item['dyn_out'] = dyn_in
                item['oid_out'] = oid_in
                item['type_out'] = 11
            elif type_in == 64:
                item['dyn_out'] = dyn_in
                item['oid_out'] = oid_in
                item['type_out'] = 12
            else:
                item['dyn_out'] = dyn_in
                item['oid_out'] = dyn_in
                item['type_out'] = 17
            url_out = f"http://api.bilibili.com/x/v2/reply?jsonp=jsonp&next=0&type={item['type_out']}&oid={item['oid_out']}&mode=3"
            yield scrapy.Request(url_out, meta={'item': item}, callback=self.count_get, dont_filter=True)

        if len(card_list)==12 :
            v_uid=item['v_uid']
            next_page_id=card_list[11]['desc']['dynamic_id']
            next_url=f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={v_uid}&offset_dynamic_id={next_page_id}"
            yield scrapy.Request(url=next_url,callback=self.parse)

    def count_get(self, response):
        item = response.meta['item']
        if json.loads(response.text)['message'] == '评论区已关闭':
            item['acount']=0
            item['count']=0
            return item
        item['acount'] = json.loads(response.text)['data']['page']['acount']
        item['count']=json.loads(response.text)['data']['page']['count']
        # page=math.ceil((item['count'])/20)+1
        self.now_len=self.now_len+1
        print('[已请求/总请求', self.now_len, '/',self.total_len, end=']')
        print('[进度: {:.2%}'.format(self.now_len / self.total_len),end=']')
        print('[正在请求的url数量：',len(self.crawler.engine.slot.inprogress),'正在队列的url数量：',len(self.crawler.engine.slot.scheduler),']')
        return item
        # for next_number in range(1,page):
        #     lz_url=f'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={next_number}&type={item["type_out"]}&oid={item["oid_out"]}&mode=3'
        #     yield scrapy.Request(url=lz_url,meta={'item':item},callback=self.reply_lz,dont_filter=True)
        # end_str = '100%'


    def reply_lz(self,response):
        try:
            test = json.loads(response.text)['data']['replies'][0]['member']['uname']
        except:
            return
        table_name=response.meta['item']['v_uid']
        dynamic_id=response.meta['item']['dyn_out']
        type_out=response.meta['item']['type_out']
        oid_out=response.meta['item']['oid_out']
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
            yield r_item
            self.total_len=self.total_len+r_item['replies']
            if r_item['replies']>0:
                rpid=reply['rpid']
                page=math.ceil(r_item['replies']/20)+1
                for next_page in range(1,page):
                    lzl_url = f'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={next_page}&type={type_out}&oid={oid_out}&ps=20&root={rpid}'
                    yield scrapy.Request(url=lzl_url,meta={'dynamic_id':r_item['dynamic'],'table_name':r_item['table_name']},callback=self.reply_lzl,dont_filter=True)

    def reply_lzl(self,response):
        try:
            test = json.loads(response.text)['data']['replies'][0]['member']['uname']
        except:
            return
        dynamic_id = response.meta['dynamic_id']
        table_name=response.meta['table_name']

        lzl_reply_list = json.loads(response.text)['data']['replies']
        for lzl_replies in lzl_reply_list:
            r_item=replyItem()
            r_item['table_name']=table_name
            r_item['r_uid'] = lzl_replies['member']['mid']
            r_item['r_name'] = lzl_replies['member']['uname']
            r_item['comment'] = lzl_replies['content']['message']
            r_item['c_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lzl_replies['ctime']))
            r_item['dynamic'] = dynamic_id
            r_item['r_type'] = '楼中楼'
            r_item['replies'] = 0
            self.now_len=self.now_len+1
            print('percent: {:.2%}'.format(self.now_len / self.total_len))
            yield r_item