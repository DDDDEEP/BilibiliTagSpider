import json
import time
from scrapy import Request, Spider
from scrapy.utils.project import get_project_settings
from BilibiliTagSpider.items import *


class TagSpider(Spider):
    name = 'tagspider'
    allowed_domains = ['bilibili.com', 'api.bilibili.com']

    newlist_url = 'https://api.bilibili.com/x/web-interface/newlist?rid={type_id}&type=0&pn={page}&ps={per_page}'
    settings = get_project_settings()
    field_map = ['aid', 'tid', 'title', 'pubdate', 'duration']
    stat_field_map = ['view', 'danmaku', 'reply',
                      'favorite', 'coin', 'share', 'like', 'dislike']

    def start_requests(self):
        type_id = self.settings.get('TYPE_ID')
        per_page = self.settings.get('PER_PAGE')
        for page in range(1, 2):
            yield Request(self.newlist_url.format(type_id=type_id, page=page, per_page=per_page),
                          callback=self.parse_newlist)

    def parse_newlist(self, response):
        """
        在时间排序API中解析视频数据
        """
        self.logger.debug(response)
        result = json.loads(response.text)
        if 'data' in result and 'archives' in result['data']:
            for video in result['data']['archives']:
                item = VideoItem()
                for field in self.field_map:
                    item[field] = video.get(field)
                for field in self.stat_field_map:
                    item[field] = video['stat'].get(field)
                item['title'] = item['title']
                item['updated_at'] = int(time.time())

                video_url = 'https://www.bilibili.com/video/av' + \
                    str(video['aid'])
                yield Request(video_url, meta={'item': item}, callback=self.parse_tag)
        else:
            print("ERROR: Newlist API Failed")

    def parse_tag(self, response):
        """
        在视频主页中解析标签
        """
        tags = response.xpath(
            r'//body/div[@id="app"]/div[@class="v-wrap"]/div[@class="l-con"]/div[@id="v_tag"]/ul/li[@class="tag"]/a/text()')

        if len(tags) == 0:
            print("ERROR: Video Page Failed -> " + response.url)
        else:
            tags = tags.extract()
            item = response.meta['item']
            item['tags'] = ','.join(tags)
            yield item
