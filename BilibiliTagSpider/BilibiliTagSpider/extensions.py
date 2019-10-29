import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.project import get_project_settings
import math

logger = logging.getLogger(__name__)


class SpiderProgressLogging(object):

    def __init__(self):
        self.items_scraped = 0
        self.settings = get_project_settings()

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # instantiate the extension object
        ext = cls()

        # connect the extension object to signals
        crawler.signals.connect(
            ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(
            ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(
            ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("爬虫启动：{}".format(spider.name))

    def spider_closed(self, spider):
        logger.info("爬虫关闭：{}".format(spider.name))

    def item_scraped(self, item, spider):
        self.items_scraped += 1
        if self.items_scraped % 500 == 0:
            total_seconds = math.ceil((spider.items_total - self.items_scraped) /
                                self.settings['PER_PAGE']) * self.settings['DOWNLOAD_DELAY']
            hours = total_seconds // 3600
            minutes = total_seconds % 3600 // 60
            seconds = total_seconds % 3600 % 60 
            logger.info(
                '爬取进度：({}/{})，{:.1f}%，预计剩余时间 {}时{}分{}秒'.format(
                    self.items_scraped,
                    spider.items_total,
                    self.items_scraped / spider.items_total * 100,
                    hours,
                    minutes,
                    seconds,
                )
            )
