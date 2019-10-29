import requests

TEST_URL = 'https://www.bilibili.com'
proxy = '210.5.10.87:53281'

proxies = {
    'http': 'http://' + proxy,
}

REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}

print(TEST_URL)
response = requests.get(TEST_URL, headers=REQUEST_HEADERS, proxies=proxies, allow_redirects=False)
# if response.status_code == 200:
#     print('Successfully')
#     print(response.text)
print(response.status_code)
p = requests.get('http://icanhazip.com', headers=REQUEST_HEADERS, proxies=proxies, allow_redirects=False)
print(p.text)



import asyncio
import aiohttp
import time
import sys
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError

async def test_single_proxy(proxy):
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = 'http://' + proxy
            # async with session.get(TEST_URL, headers=REQUEST_HEADERS, proxy=real_proxy, timeout=5, allow_redirects=False) as response:
            async with session.get(TEST_URL, headers=REQUEST_HEADERS, proxy=real_proxy, allow_redirects=False) as response:
                print(response.status)
        except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError) as e:
            print(proxy, repr(e))

loop = asyncio.get_event_loop()
tasks = [test_single_proxy(proxy)]
loop.run_until_complete(asyncio.wait(tasks))