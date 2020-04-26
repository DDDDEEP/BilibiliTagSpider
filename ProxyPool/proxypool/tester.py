import sys
import time
import logging
import asyncio
import aiohttp

from proxypool.db import RedisClient
import proxypool.setting as setting

logger = logging.getLogger('ProxyPool')


class Tester(object):
    """代理可用性测试器"""
    def __init__(self, proxy_key=setting.REDIS_KEY):
        self.redis = RedisClient(proxy_key=proxy_key)

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                if not proxy.startswith('http://'):
                    proxy = 'http://' + proxy
                async with session.get(setting.TEST_URL,
                                       headers=setting.REQUEST_HEADERS,
                                       proxy=proxy,
                                       timeout=5,
                                       allow_redirects=False) as response:
                    if response.status in setting.VALID_STATUS_CODES:
                        self.redis.set_proxy_max(proxy)
                        logger.info('代理 {} 请求成功，响应码为 {}'.format(
                            proxy, response.status))
                    else:
                        self.redis.decrease_proxy(proxy)
                        logger.info('代理 {} 的响应码不合法，为 {}'.format(
                            proxy, response.status))
            except (aiohttp.ClientError,
                    aiohttp.client_exceptions.ClientConnectorError,
                    asyncio.TimeoutError, AttributeError) as e:
                self.redis.decrease_proxy(proxy)
                logger.warning('代理 {} 请求出错：{}'.format(proxy, repr(e)))

    def run(self):
        """
        测试主函数
        :return:
        """
        logger.info('测试器开始运行')
        try:
            count = self.redis.get_count()
            logger.info('当前有 {} 个代理'.format(count))
            for i in range(0, count, setting.BATCH_TEST_SIZE):
                start = i
                stop = min(i + setting.BATCH_TEST_SIZE, count)
                logger.info('正在测试第 {}-{} 个代理'.format(start + 1, stop))
                test_proxies = self.redis.get_batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [
                    self.test_single_proxy(proxy) for proxy in test_proxies
                ]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            logger.error('测试器发生错误')
