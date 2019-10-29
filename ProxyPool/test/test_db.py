import unittest
import logging

from proxypool.db import RedisClient
from proxypool.setting import *
import logging
logger = logging.getLogger('ProxyPool')

class TestRedisClient(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRedisClient, self).__init__(*args, **kwargs)
        self.redis = RedisClient(proxy_key=TEST_REDIS_KEY)

    def setUp(self):
        self.redis.clear()
        print('')

    def tearDown(self):
        self.redis.clear()

    def test_add_proxy(self):
        self.redis.add_proxy('0.0.0.0:0', 10)
        self.redis.add_proxy('0.0.0.0', 10)
        self.assertTrue(self.redis.exist_proxy('0.0.0.0:0'))
        self.assertEqual(self.redis.get_count(), 1)

    def test_get_random(self):
        count = 10
        for i in range(count):
            self.redis.add_proxy('0.0.0.0:' + str(i), i)
        self.redis.set_proxy_max('0.0.0.0:0')

        # 获取到的是分数最大的代理
        self.assertEqual(self.redis.get_random(), '0.0.0.0:0')

        # 不存在分数最大的代理时，随机获取前100名的代理
        times = 5
        self.redis.decrease_proxy('0.0.0.0:0')
        print('不存在分数最大代理时，随机获取', times, '个代理：')
        for i in range(times):
            print(self.redis.get_random())
