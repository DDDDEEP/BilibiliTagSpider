import unittest

from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.setting import *
import logging
logger = logging.getLogger('ProxyPool')

class TestRedisClient(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRedisClient, self).__init__(*args, **kwargs)
        self.getter = Getter(proxy_key=TEST_REDIS_KEY)
        self.tester = Tester(proxy_key=TEST_REDIS_KEY)

    def setUp(self):
        self.getter.redis.clear()
        print('')

    def tearDown(self):
        self.getter.redis.clear()

    def test_run(self):
        self.getter.run()
        logger.info('本次测试获取 {} 个代理'.format(self.getter.redis.get_count()))
        self.tester.run()
