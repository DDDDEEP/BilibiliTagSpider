#!/usr/bin/env python
"""分布式爬虫启动脚本，管理start_urls队列。"""

import argparse
import math
import redis
import requests
import time

from BilibiliTagSpider import settings
from helpers import print_time

# 命令行参数
#     - type_id   -- 分区id
#     - time-from -- 起始日期（输入格式yyyyMMdd)
#     - time-to   -- 结束日期
parser = argparse.ArgumentParser()
parser.add_argument('--type-id', type=int, default=0)
parser.add_argument('--time-from', type=str, default='20100101')
parser.add_argument('--time-to', type=str, default='20100101')
args = parser.parse_args()

type_id = int(args.type_id)
time_from = int(args.time_from)
time_to = int(args.time_to)
time_start = time.time()

# 请求热度排行api，获取分页数据量
hotlist_url = "https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=pubdate&copy_right=-1&"
hotlist_url += "cate_id={type_id}&page={page}&pagesize={per_page}&time_from={time_from}&time_to={time_to}"
response = requests.get(
    hotlist_url.format(type_id=type_id,
                       page=1,
                       per_page=1,
                       time_from=time_from,
                       time_to=time_to)).json()
per_page = settings.PER_PAGE
pages = math.ceil(response['numResults'] / per_page)
num_results = response['numResults']
print(
    "分区号{type_id}, [{time_from}-{time_to}]共有{num_results}个视频，{pages}页，每页{per_page}个视频"
    .format(
        type_id=type_id,
        time_from=time_from,
        time_to=time_to,
        num_results=num_results,
        pages=pages,
        per_page=per_page,
    ))

# 向Redis的start_urls键添加url
REDIS_START_URL_KEY = 'tag_redis_spider:start_urls'
REDIS_ITEMS_KEY = 'tag_redis_spider:items'
conn = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    password=settings.REDIS_PARAMS['password'],
    decode_responses=True  # 设置为True返回的数据格式就是时str类型
)
conn.delete(REDIS_START_URL_KEY)
conn.delete(REDIS_ITEMS_KEY)
for index in range(1, pages + 1):
    url = hotlist_url.format(type_id=type_id,
                             page=index,
                             per_page=per_page,
                             time_from=time_from,
                             time_to=time_to)
    conn.rpush(REDIS_START_URL_KEY, url)

# 监控爬虫进度
url_len = conn.llen(REDIS_START_URL_KEY)
item_len = conn.llen(REDIS_ITEMS_KEY)
while url_len != 0:
    time.sleep(2)
    url_len = conn.llen(REDIS_START_URL_KEY)
    item_len = conn.llen(REDIS_ITEMS_KEY)
    # print("总爬取进度：({}/{})，{:.1f}%".format(
    #     item_len,
    #     num_results,
    #     item_len / num_results * 100,
    # ))
    print("剩余urls：{}".format(url_len))

print(
    "分区号{type_id}, [{time_from}-{time_to}]共有{num_results}个视频，{pages}页，每页{per_page}个视频"
    .format(
        type_id=type_id,
        time_from=time_from,
        time_to=time_to,
        num_results=response['numResults'],
        pages=pages,
        per_page=per_page,
    ))
print_time("爬取所用时间：", time.time() - time_start)

# TODO 插入记录每日视频爬取完成的record项
