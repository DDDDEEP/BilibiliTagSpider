
import sys
import logging
import requests
from requests.auth import HTTPBasicAuth

from proxypool.db import RedisClient
import proxypool.setting as setting

logger = logging.getLogger('ProxyPool')


class Getter():
    """代理获取器"""
    def __init__(self, proxy_key=setting.REDIS_KEY):
        self.redis = RedisClient(proxy_key=proxy_key)
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.get_count() >= setting.POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        logger.info('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]

                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add_proxy(proxy, setting.INITIAL_SCORE)


class ProxyMetaclass(type):
    # 获取代理的元类
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    # 获取代理的方法集合
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            logger.info('成功获取到代理：{}'.format(proxy))
            proxies.append(proxy)
        return proxies

    def crawl_custom_proxy(self):
        response = requests.get(
            setting.CUSTOM_PROXY_URL,
            auth=HTTPBasicAuth(setting.PROXY_USER, setting.PROXY_PASSWORD)
        ).json()
        for proxy_data in response:
            yield proxy_data['proxy']

    # 以下都是免费代理方法，可用性较低
    # def crawl_daili66(self, page_count=4):
    #     """
    #     获取代理66
    #     :param page_count: 页码
    #     :return: 代理
    #     """
    #     crawl_66ip = crawl_66ip_page.Crawl_66ip()
    #     start_url = 'http://www.66ip.cn/{}.html'
    #     urls = [start_url.format(page) for page in range(1, page_count + 1)]
    #     for url in urls:
    #         print('Crawling', url)
    #         html = crawl_66ip.get_url(url)
    #         soup = BeautifulSoup(html, 'lxml')
    #         div = soup.find('div', class_="containerbox boxindex")
    #         trs = div.find_all('tr')
    #         for tr in trs[1:]:
    #             tds = tr.find_all('td')
    #             ip = tds[0].string
    #             port = tds[1].string
    #             yield ':'.join([ip, port])

    # def crawl_ip3366(self):
    #     for page in range(1, 4):
    #         start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(
    #             page)
    #         html = get_page(start_url)
    #         ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
    #         # \s * 匹配空格，起到换行作用
    #         re_ip_address = ip_address.findall(html)
    #         for address, port in re_ip_address:
    #             result = address + ':' + port
    #             yield result.replace(' ', '')

    # def crawl_kuaidaili(self):
    #     for i in range(1, 4):
    #         start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address = re.compile('<td data-title="IP">(.*?)</td>')
    #             re_ip_address = ip_address.findall(html)
    #             port = re.compile('<td data-title="PORT">(.*?)</td>')
    #             re_port = port.findall(html)
    #             for address, port in zip(re_ip_address, re_port):
    #                 address_port = address + ':' + port
    #                 yield address_port.replace(' ', '')
    #         time.sleep(3)

    # def crawl_xicidaili(self):
    #     for i in range(1, 4):
    #         start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
    #         headers = {
    #             'Accept':
    #             'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #             'Cookie':
    #             '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
    #             'Host': 'www.xicidaili.com',
    #             'Referer': 'http://www.xicidaili.com/nn/3',
    #             'Upgrade-Insecure-Requests': '1',
    #         }
    #         html = get_page(start_url, options=headers)
    #         if html:
    #             find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
    #             trs = find_trs.findall(html)
    #             for tr in trs:
    #                 find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
    #                 re_ip_address = find_ip.findall(tr)
    #                 find_port = re.compile('<td>(\d+)</td>')
    #                 re_port = find_port.findall(tr)
    #                 for address, port in zip(re_ip_address, re_port):
    #                     address_port = address + ':' + port
    #                     yield address_port.replace(' ', '')

    # def crawl_feiyiproxy(self):
    #     start_url = 'http://www.feiyiproxy.com/'
    #     headers = {
    #         'User-Agent':
    #         'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
    #                     Chrome/63.0.3239.132 Safari/537.36',
    #         'Referer': 'http://www.feiyiproxy.com/?b_scene_zt=1'
    #     }
    #     data = {'page_id': '1457'}
    #     resp = requests.get(start_url, headers=headers, params=data)
    #     html = resp.text
    #     soup = BeautifulSoup(html, 'lxml')
    #     table = soup.find('table')
    #     trs = table.find_all('tr')
    #     for tr in trs[1:]:
    #         tds = tr.find_all('td')
    #         ip = tds[0].string
    #         port = tds[1].string
    #         result = ':'.join([ip, port])
    #         yield result

    # def crawl_data5u(self):
    #     start_url = 'http://www.data5u.com/'
    #     headers = {
    #         'User-Agent':
    #         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) \
    #         Chrome/63.0.3239.108 Safari/537.36',
    #     }
    #     html = get_page(start_url, options=headers)
    #     if html:
    #         ip_address = re.compile(
    #             '<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>',
    #             re.S)
    #         re_ip_address = ip_address.findall(html)
    #         for address, port in re_ip_address:
    #             result = address + ':' + port
    #             yield result.replace(' ', '')
