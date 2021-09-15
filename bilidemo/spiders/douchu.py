# -*- coding: utf-8 -*-
import scrapy
import math
from bs4 import BeautifulSoup
from ..items import douchuItem
import time

class DouchuSpider(scrapy.Spider):
    name = 'douchu'
    allowed_domains = ['douban.com']
    # log-时间记录
    t1 = time.time()
    start_time = t1
    # log-长度记录
    starts=range(0,120000,25)
    total_len=math.ceil(120000/25)
    now_len_bz=0
    start_urls = [f'https://www.douban.com/group/a-soul/discussion?start={start}' for start in starts]

    def parse(self, response):
        self.now_len_bz = (self.now_len_bz + 1)
        avg_time=(time.time() - self.start_time) / self.now_len_bz
        pre_time=(self.total_len-self.now_len_bz)*avg_time
        print('[完/总', self.now_len_bz, '/', self.total_len, end=']')
        print('[进度: {:.2%}'.format(self.now_len_bz / self.total_len), end=']')
        print(f'[平均时间：{avg_time}',end=']')
        print(f'[每秒并发：{1/avg_time}', end=']')
        print(f'[剩余{pre_time/60}分完成',end=']')
        print('[正在请求：',len (self.crawler.engine.slot.inprogress), '正在队列：',len(self.crawler.engine.slot.scheduler),']')
        tie_list=BeautifulSoup(str(BeautifulSoup(response.text,'lxml').find_all('table','olt')),'lxml').find_all('tr')
        for tie in tie_list[1:]:
            r_item = douchuItem()
            r_item['title']=tie.find_all('td')[0].text.replace('\n', '').replace(' ', '').replace('无关水', '').replace('丨','').replace('‖', '')
            r_item['author']=tie.find_all('td')[1].text.replace('\n', '')
            r_item['replies']=tie.find_all('td')[2].text
            r_item['e_time']=tie.find_all('td')[3].text
            r_item['url'] = tie.find_all('td')[0].find_all('a')[0].get('href')
            yield r_item
