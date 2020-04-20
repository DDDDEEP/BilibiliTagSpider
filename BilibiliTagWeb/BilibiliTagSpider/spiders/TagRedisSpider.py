import json
import time
import urllib.parse as urlparse
from urllib.parse import parse_qs

from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import RedisSpider

from ..items import VideoItem
from helpers import stat_to_int


class TagRedisSpider(RedisSpider):
    """使用scrapy-redis的爬虫"""
    name = "tag_redis_spider"
    redis_key = 'tag_redis_spider:start_urls'
    allowed_domains = [
        "bilibili.com",
    ]

    def __init__(self, *args, **kwargs):
        super(TagRedisSpider, self).__init__(*args, **kwargs)
        self.settings = get_project_settings()

    def parse(self, response):
        """
        在热度排序API的返回结果中，解析视频数据
        """
        parsed = urlparse.urlparse(response.url)
        param_list = parse_qs(parsed.query)
        type_id = int(param_list['cate_id'][0])

        self.logger.info("parse_hotlist_one_day_page，得到回应：{}".format(
            response.url))
        result = json.loads(response.text)
        if 'result' in result and 'numPages' in result:
            for video in result['result']:
                pubdate_arr = time.strptime(video['pubdate'],
                                            '%Y-%m-%d %H:%M:%S')
                pubdate = int(time.mktime(pubdate_arr))
                created_time = int(time.time())
                # TODO:部分stat数据需用另外的接口获取，之后的开发扩展再补充
                item = VideoItem(
                    aid=video['id'],
                    tid=type_id,
                    title=video['title'],
                    pubdate=pubdate,
                    duration=video['duration'],
                    created_at=created_time,
                    updated_at=created_time,
                    tags=video['tag'],
                    stat_view=stat_to_int(video['play']),
                    stat_danmaku=stat_to_int(video['video_review']),
                    stat_reply=stat_to_int(video['review']),
                    stat_favorite=stat_to_int(video['favorites']),
                    stat_coin=0,
                    stat_share=0,
                    stat_like=0,
                    stat_dislike=0,
                )
                yield item
        else:
            self.logger.error("parse_hotlist_one_day_page，热榜列表解析失败：{}".format(
                response.url))

    def errback_common(self, failure):
        self.logger.error("url请求出错：{}, {}".format(failure.request.url,
                                                  repr(failure)))
