import redis
import logging
from proxypool.error import PoolEmptyError
from proxypool.setting import *
from random import choice
import re

logger = logging.getLogger('ProxyPool')

# Redis操作封装类


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, proxy_key=REDIS_KEY):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(
            host=host, port=port, password=password, decode_responses=True)
        self.proxy_key = proxy_key

    def add_proxy(self, proxy, score):
        """
        添加代理
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            logger.info('代理 {} 不符合规范'.format(proxy))
            return
        if not self.db.zscore(self.proxy_key, proxy):
            return self.db.zadd(self.proxy_key, {proxy: score})

    def get_random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(self.proxy_key, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(self.proxy_key, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease_proxy(self, proxy):
        """
        代理失败，减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(self.proxy_key, proxy)
        if score and score > MIN_SCORE:
            return self.db.zincrby(self.proxy_key, -1, proxy)
        else:
            logger.info('代理 {} 减分，当前分数：{}，移除'.format(proxy, score))
            return self.db.zrem(self.proxy_key, proxy)

    def exist_proxy(self, proxy):
        """
        判断代理是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(self.proxy_key, proxy) == None

    def set_proxy_max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        logger.info('代理 {} 可用，设置为 {}'.format(proxy, MAX_SCORE))
        return self.db.zadd(self.proxy_key, {proxy: MAX_SCORE})

    def get_count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(self.proxy_key)

    def get_all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(self.proxy_key, MIN_SCORE, MAX_SCORE)

    def get_batch(self, start, stop):
        """
        获取数量区间的代理
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(self.proxy_key, start, stop - 1)

    def clear(self):
        self.db.delete(self.proxy_key)
