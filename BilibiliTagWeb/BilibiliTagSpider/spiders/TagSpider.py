import json
import math
import time

from scrapy import Request, Spider
from scrapy.utils.project import get_project_settings

from ..items import VideoItem, RecordItem
from helpers import date_to_timestamp, timestamp_to_date, stat_to_int, RecordStatus


class TagSpider(Spider):
    name = "tag_spider"
    allowed_domains = [
        "bilibili.com",
    ]

    def __init__(self,
                 type_id=None,
                 time_from=None,
                 time_to=None,
                 *args,
                 **kwargs):
        super(TagSpider, self).__init__(*args, **kwargs)
        self.newlist_url = "http://api.bilibili.com/x/web-interface/newlist?rid={type_id}&type=0&pn={page}&ps={per_page}"
        self.video_url = "http://www.bilibili.com/video/av{aid}"
        self.stat_url = "http://api.bilibili.com/x/web-interface/archive/stat?aid={aid}"
        self.hotlist_url = "http://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=pubdate&copy_right=-1&"
        self.hotlist_url += "cate_id={type_id}&page={page}&pagesize={per_page}&time_from={time_from}&time_to={time_to}"
        self.settings = get_project_settings()

        self.items_total = 0  # 需爬取的视频总数
        self.parse_items_total = {}  # 各日期已爬取的视频总数
        self.TYPE_ID = int(type_id)  # 分区id
        self.TIME_FROM = int(time_from)  # 起始日期
        self.TIME_TO = int(time_to)  # 结束日期

    def start_requests(self):
        """
        通过热度排行API，获取视频总数，再进行后续分类解析
        """
        if self.TIME_FROM == self.TIME_TO:
            # 如果前后日期相同，则直接请求当日的分页数据，防止Scrapy过滤重复请求
            yield Request(self.hotlist_url.format(type_id=self.TYPE_ID,
                                                  page=1,
                                                  per_page=1,
                                                  time_from=self.TIME_FROM,
                                                  time_to=self.TIME_FROM),
                          meta={
                              'time_cur': self.TIME_FROM,
                              'time_from_equal_to': True
                          },
                          callback=self.parse_hotlist_one_day,
                          errback=self.errback_common)
        else:
            yield Request(self.hotlist_url.format(type_id=self.TYPE_ID,
                                                  page=1,
                                                  per_page=1,
                                                  time_from=self.TIME_FROM,
                                                  time_to=self.TIME_TO),
                          callback=self.parse_hotlist_init,
                          errback=self.errback_common)

    def parse_hotlist_init(self, response):
        """
        通过热度排行API，按日期排序，获取视频总数，然后分日期进行爬取
        """
        self.logger.info("parse_hotlist_init，得到回应：{}".format(response.url))
        result = json.loads(response.text)
        if 'numResults' in result and result['numResults'] >= 0:
            self.items_total = result['numResults']
            self.logger.info(
                "[分区号{type_id}，{time_from}-{time_to}]的总视频数为{total}".format(
                    type_id=self.TYPE_ID,
                    time_from=self.TIME_FROM,
                    time_to=self.TIME_TO,
                    total=result['numResults'],
                ))

            # 处理得到范围内每日的yyyyMMdd日期，分别进行请求
            timestamp_time_from = date_to_timestamp(self.TIME_FROM)
            timestamp_time_to = date_to_timestamp(self.TIME_TO)
            timestamp_cur = timestamp_time_from
            while (timestamp_cur <= timestamp_time_to):
                time_cur = timestamp_to_date(timestamp_cur)
                yield Request(self.hotlist_url.format(type_id=self.TYPE_ID,
                                                      page=1,
                                                      per_page=1,
                                                      time_from=time_cur,
                                                      time_to=time_cur),
                              meta={'time_cur': time_cur},
                              callback=self.parse_hotlist_one_day,
                              errback=self.errback_common)
                timestamp_cur += 86400
        else:
            self.logger.error("parse_hotlist_init，热榜分页信息解析失败：{}".format(
                response.url))

    def parse_hotlist_one_day(self, response):
        """
        同一日期下，依次请求热度排行api，按日期排序的各页号的数据，进行爬取
        """
        self.logger.info("parse_hotlist_one_day，得到回应：{}".format(response.url))
        result = json.loads(response.text)
        if 'numResults' in result and result['numResults'] >= 0:
            time_cur = response.meta['time_cur']
            day_total_page = math.ceil(result['numResults'] /
                                       self.settings['PER_PAGE'])
            self.parse_items_total[time_cur] = {
                'cur': 0,
                'total': result['numResults']
            }

            if 'time_from_equal_to' in response.meta and response.meta[
                    'time_from_equal_to']:
                self.logger.info(
                    "[分区号{type_id}，{time_from}-{time_to}]的总视频数为{total}".format(
                        type_id=self.TYPE_ID,
                        time_from=self.TIME_FROM,
                        time_to=self.TIME_TO,
                        total=result['numResults'],
                    ))
                self.items_total = result['numResults']

            self.logger.info(
                "[分区号{type_id}，{time_cur}]的视频数为{total}，分页为每页{per_page}个，共{total_page}页，请求延迟为{delay}s"
                .format(
                    type_id=self.TYPE_ID,
                    time_cur=time_cur,
                    total=result['numResults'],
                    per_page=self.settings['PER_PAGE'],
                    total_page=day_total_page,
                    delay=self.settings['DOWNLOAD_DELAY'],
                ))

            # 依次请求对应各页号的数据
            cur_page = 1
            while (cur_page <= day_total_page):
                yield Request(self.hotlist_url.format(
                    type_id=self.TYPE_ID,
                    page=cur_page,
                    per_page=self.settings['PER_PAGE'],
                    time_from=response.meta['time_cur'],
                    time_to=response.meta['time_cur'],
                ),
                              meta={
                                  'time_cur': time_cur,
                              },
                              callback=self.parse_hotlist_one_day_page,
                              errback=self.errback_common)
                cur_page += 1
        else:
            self.logger.error("parse_hotlist_one_day，热榜分页信息解析失败：{}".format(
                response.url))

    def parse_hotlist_one_day_page(self, response):
        """
        在热度排序API的返回结果中，解析视频数据
        """
        self.logger.info("parse_hotlist_one_day_page，得到回应：{}".format(
            response.url))
        result = json.loads(response.text)
        if 'result' in result and 'numPages' in result:
            time_cur = response.meta['time_cur']
            for video in result['result']:
                pubdate_arr = time.strptime(video['pubdate'],
                                            '%Y-%m-%d %H:%M:%S')
                pubdate = int(time.mktime(pubdate_arr))
                created_time = int(time.time())
                # TODO:部分stat数据需用另外的接口获取，之后的开发扩展再补充
                item = VideoItem(
                    aid=video['id'],
                    tid=self.TYPE_ID,
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
                self.parse_items_total[time_cur]['cur'] += 1

            # 记录该日爬取已完成
            if self.parse_items_total[time_cur][
                    'cur'] == self.parse_items_total[time_cur]['total']:
                item = RecordItem(tid=self.TYPE_ID,
                                  pubdate=date_to_timestamp(
                                      response.meta['time_cur']),
                                  status=RecordStatus.Crawled.value)
                yield item
                self.logger.info("[分区号{type_id}，{time_cur}]的视频爬取完成".format(
                    type_id=self.TYPE_ID,
                    time_cur=time_cur,
                ))
        else:
            self.logger.error("parse_hotlist_one_day_page，热榜列表解析失败：{}".format(
                response.url))

    def parse_tag_from_videopage(self, response):
        """
        在视频主页中解析标签
        """
        tags = response.xpath(
            r'//body/div[@id="app"]/div[@class="v-wrap"]/div[@class="l-con"]/div[@id="v_tag"]/ul/li[@class="tag"]/a/text()'
        )

        if len(tags) == 0:
            self.logger.error("视频主页解析标签失败：{}".format(response.url))
        else:
            tags = tags.extract()
            item = response.meta['item']
            item['tags'] = ','.join(tags)
            yield item

    def errback_common(self, failure):
        self.logger.error("url请求出错：{}, {}".format(failure.request.url,
                                                  repr(failure)))
