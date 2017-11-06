#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-04 17:44:17
# Project: TouTiaocomment

from pyspider.libs.base_handler import *
from fake_useragent import UserAgent
import time
import hashlib
from pyspider.database.mysql.selfmysqldb import SQL 
# from pyspider.result import ResultWorker


class Handler(BaseHandler):
    ua = UserAgent()
    crawl_config = {
        'headers': {'User-Agent': ua.random}
    }
    
    feed_url = 'https://www.toutiao.com/api/pc/feed/'
    sql=SQL()

    def getASCP(self):
        t = round(time.time())
        e = hex(t).upper()[2:]
        m = hashlib.md5()
        m.update(str(t).encode(encoding='utf-8'))
        i = m.hexdigest().upper()

        if len(e) != 8:
            AS = '479BB4B7254C150'
            CP = '7E0AC8874BB0985'
            return AS, CP

        n = i[0:5]
        a = i[-5:]
        s = ''
        r = ''
        for o in range(5):
            s += n[o] + e[o]
            r += e[o + 3] + a[o]

        AS = 'A1' + s + e[-3:]
        CP = e[0:3] + r + 'E1'
        return AS, CP
    

    @every(minutes=24 * 60)
    def on_start(self, maxtime=0):
        AS, CP = self.getASCP()
        
        payloads = {'max_behot_time': maxtime, 'category': '__all__','utm_source': 'toutiao', 'widen': 1, 'tadrequire': 'false', 'as': AS, 'cp': CP}
        self.crawl(self.feed_url, params=payloads,
                   callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
          rj=response.json
          for i in rj.get('data', None):
            if i.get('is_feed_ad') == False:
                result= {'title': i.get('title'), 'tags': i.get('chinese_tag'), 'comments': i.get('comments_count'),'url': 'https://www.toutiao.com'+i.get('source_url')}
                print(result)
                self.sql.insert('toutiaocomment', **result)
          
          if rj.get('next'):
            maxtime = rj.get('next').get('max_behot_time')
            AS, CP = self.getASCP()
            payloads = {'max_behot_time': maxtime, 'category': '__all__','utm_source': 'toutiao', 'widen': 1, 'tadrequire': 'false', 'as': AS, 'cp': CP}
            self.crawl(self.feed_url, params=payloads,callback=self.index_page)
            
