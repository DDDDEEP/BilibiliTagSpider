import logging
import requests
from requests.exceptions import ConnectionError

logger = logging.getLogger('ProxyPool')

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    headers = dict(base_headers, **options)
    logger.info('正在抓取代理 {}'.format(url))
    try:
        response = requests.get(url, headers=headers)
        logger.info('抓取代理成功 {} {}'.format(url, response.status_code))
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        logger.info('代理抓取失败 {}'.format(url))
        return None
