# encoding=utf-8

import redis
import aioredis
import asyncio
from hashlib import md5
import logging
logging.basicConfig(level=1)
LOGGER = logging.getLogger(__name__)

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self,fetch_q,bloom_q, host='', port=6379, password='', db=0, blockNum=1, key='blfilter',loop=None,):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param blockNum: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        self.loop=loop
        # self.pool = redis.ConnectionPool(host=host, port=port, password=password,db=db)        
        # self.server=redis.StrictRedis(connection_pool=self.pool)
        self.server= None
        self.bloom_q=bloom_q
        self.fetch_q=fetch_q
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    async def isContains(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input.encode('utf-8'))
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            # ret = ret & self.server.getbit(name, loc)
            ret = ret & await self.server.execute("getbit",name,loc)

        return ret

    async def insert(self, str_input):
        m5 = md5()
        m5.update(str_input.encode('utf-8'))
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            # self.server.setbit(name, loc, 1)
            await self.server.execute("setbit",name,loc,1)

    async def workers(self):
        try:
            while 1:
                url=await self.bloom_q.get()
                if not await self.isContains(url):
                    await self.insert(url)
                    LOGGER.info('加入url %r', url)
                    self.fetch_q.put_nowait(url)
                    self.bloom_q.task_done()
        except asyncio.CancelledError:
            pass


    async def run(self):
        self.server= await aioredis.create_pool(("133.133.133.133",6379),password="133")

        works=[asyncio.ensure_future(self.workers(),loop=self.loop) for _ in range(4)]
        await self.bloom_q.join()
        for w in works:
            w.cancel()



# if __name__ == '__main__':
#     """ 第一次运行时会显示 not exists!，之后再运行会显示 exists! """
#     loop=asyncio.get_event_loop
#     bf = BloomFilter()
#     loop.run_forever()
#     if bf.isContains('http://www.baidu12.com'):   # 判断字符串是否存在
#         print ('exists!')
#     else:
#         print ('not exists!')
#         bf.insert('http://www.baidu12.com')