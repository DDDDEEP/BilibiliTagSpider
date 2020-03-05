import json
import time
import math
import logging
import requests
from scrapy import Request, Spider
from scrapy.utils.project import get_project_settings
from BilibiliTagSpider.items import *


def stat_to_int(val):
    return (val if val != '--' else -1)


class TagSpider(Spider):
    name = 'tagspider'
    allowed_domains = ['bilibili.com']

    def __init__(self, *args, **kwargs):
        
        super(TagSpider, self).__init__()
        self.newlist_url = 'https://api.bilibili.com/x/web-interface/newlist?rid={type_id}&type=0&pn={page}&ps={per_page}'
        self.video_url = 'https://www.bilibili.com/video/av{aid}'
        self.stat_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={aid}'
        self.hotlist_url = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=pubdate&copy_right=-1&'
        self.hotlist_url += 'cate_id={type_id}&page={page}&pagesize={per_page}&time_from={time_from}&time_to={time_to}'
        self.settings = get_project_settings()
        self.items_total = 0

    def start_requests(self):
        # 通过硬币热榜API爬取，首先获取数据分页信息
        type_id = self.settings['TYPE_ID']
        yield Request(self.hotlist_url.format(type_id=type_id,
                                              page=1,
                                              per_page=1,
                                              time_from=self.settings['TIME_FROM'],
                                              time_to=self.settings['TIME_TO']),
                      meta={'tid': type_id},
                      callback=self.parse_hotlist_page,
                      errback=self.errback_common)

        # 通过时间排序API爬取
        # for page in range(1, 10):
        #     yield Request(self.newlist_url.format(type_id=type_id, page=page, per_page=per_page),
        #                   callback=self.parse_newlist,
        #                   errback=self.errback_common)
        #             for page in range(1, 10):

    def parse_hotlist_page(self, response):
        """
        单独调用热度排序API，获取分页数据，依次请求对应页号的数据
        """
        self.logger.info('得到回应：{}'.format(response.url))
        result = json.loads(response.text)
        if 'numResults' in result and result['numResults'] >= 0:
            self.items_total = result['numResults']
            total_page = math.ceil(
                result['numResults'] / self.settings['PER_PAGE'])
            cur_page = 1
            self.logger.info(
                "({time_from}-{time_to})的视频数为{total}，分页为每页{per_page}个，共{page}页，请求延迟为{delay}s".format(
                    time_from=self.settings['TIME_FROM'],
                    time_to=self.settings['TIME_TO'],
                    total=result['numResults'],
                    per_page=self.settings['PER_PAGE'],
                    page=total_page,
                    delay=self.settings['DOWNLOAD_DELAY'],
                )
            )
            while (cur_page <= total_page):
                yield Request(self.hotlist_url.format(type_id=response.meta['tid'],
                                                      page=cur_page,
                                                      per_page=self.settings['PER_PAGE'],
                                                      time_from=self.settings['TIME_FROM'],
                                                      time_to=self.settings['TIME_TO']),
                              meta={'tid': response.meta['tid']},
                              callback=self.parse_hotlist,
                              errback=self.errback_common)
                cur_page += 1
        else:
            self.logger.error("热榜分页信息解析失败：{}".format(response.url))

    def parse_hotlist(self, response):
        """
        在热度排序API中解析视频数据
        """
        self.logger.info('得到回应：{}'.format(response.url))
        result = json.loads(response.text)
        if 'result' in result:
            for video in result['result']:
                pubdate_arr = time.strptime(
                    video['pubdate'], "%Y-%m-%d %H:%M:%S")
                pubdate = int(time.mktime(pubdate_arr))
                created_time = int(time.time())
                # TODO:部分stat数据无法获取，之后的开发扩展再补充
                # 播放量可能为'--'，为方便后续处理，将其清洗为-1
                item = VideoItem(aid=video['id'],
                                 tid=response.meta['tid'],
                                 title=video['title'],
                                 pubdate=pubdate,
                                 duration=video['duration'],
                                 created_at=created_time,
                                 updated_at=created_time,
                                 tags=video['tag'],
                                 stat_view=int(stat_to_int(video['play'])),
                                 stat_danmaku=int(stat_to_int(video['video_review'])),
                                 stat_reply=int(stat_to_int(video['review'])),
                                 stat_favorite=int(stat_to_int(video['favorites'])),
                                 stat_coin=0,
                                 stat_share=0,
                                 stat_like=0,
                                 stat_dislike=0,)
                yield item
        else:
            self.logger.error("热榜列表解析失败：{}".format(response.url))

    def parse_newlist(self, response):
        """
        在时间排序API中解析视频数据
        """
        result = json.loads(response.text)
        if 'data' in result and 'archives' in result['data']:
            for video in result['data']['archives']:
                item = VideoItem(aid=video['aid'],
                                 tid=video['tid'],
                                 title=video['title'],
                                 pubdate=video['pubdate'],
                                 duration=video['duration'],
                                 updated_at=int(time.time()),
                                 stat_view=stat_to_int(video['stat']['view']),
                                 stat_danmaku=stat_to_int(
                                     video['stat']['danmaku']),
                                 stat_reply=video['stat']['reply'],
                                 stat_favorite=video['stat']['favorite'],
                                 stat_coin=video['stat']['coin'],
                                 stat_share=video['stat']['share'],
                                 stat_like=video['stat']['like'],
                                 stat_dislike=video['stat']['dislike'],)

                yield Request(self.video_url.format(aid=video['aid']),
                              meta={'item': item},
                              callback=self.parse_tag_from_videopage,
                              errback=self.errback_common)
        else:
            self.logger.error("视频投稿列表解析失败：{}".format(response.url))

    def parse_tag_from_videopage(self, response):
        """
        在视频主页中解析标签
        """
        tags = response.xpath(
            r'//body/div[@id="app"]/div[@class="v-wrap"]/div[@class="l-con"]/div[@id="v_tag"]/ul/li[@class="tag"]/a/text()')

        if len(tags) == 0:
            self.logger.error("视频主页解析标签失败：{}".format(response.url))
        else:
            tags = tags.extract()
            item = response.meta['item']
            item['tags'] = ','.join(tags)
            yield item

    def errback_common(self, failure):
        self.logger.error('url请求出错：{}, {}'.format(
            failure.request.url, repr(failure)))
