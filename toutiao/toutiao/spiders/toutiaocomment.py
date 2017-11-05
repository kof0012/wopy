# -*- coding: utf-8 -*-
import scrapy
from fake_useragent import UserAgent
import time
import hashlib
import json
from toutiao.items import ToutiaoItem
class ToutiaocommentSpider(scrapy.Spider):
    name = 'toutiaocomment'
    allowed_domains = ['toutiao.com']
    feed_url = "https://www.toutiao.com/api/pc/feed/?max_behot_time={0}&category=__all__&utm_source=toutiao&widen=1&tadrequire=false&as={1}&cp={2}"
    ua=UserAgent()
    headers={'User-Agent': ua.random}

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

    def start_requests(self):
        return [scrapy.Request(self.feed_url.format(0,self.getASCP()[0],self.getASCP()[1]),headers=self.headers)]
    
    def parse(self, response):
        rj=json.loads(response.text)
        for i in rj.get('data', None):
            if i.get('is_feed_ad') == False:
                ttitem= ToutiaoItem()
                ttitem['title'] = i.get('title')
                ttitem['tags'] = i.get('chinese_tag')
                ttitem['comments'] = i.get('comments_count')
                ttitem['url'] = 'https://www.toutiao.com'+i.get('source_url')
                yield ttitem

        
        if rj.get('next'):
            maxtime = rj.get('next').get('max_behot_time')
            yield scrapy.Request(self.feed_url.format(maxtime,self.getASCP()[0],self.getASCP()[1]),headers=self.headers,callback=self.parse)
        else:
            yield scrapy.Request(self.feed_url.format(0,self.getASCP()[0],self.getASCP()[1]),headers=self.headers,callback=self.parse,dont_filter=True)

                
            
       
        
        
