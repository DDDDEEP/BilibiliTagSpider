import math
import logging
import pprint
import time

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.project import get_project_settings
from twisted.internet.task import LoopingCall

from helpers import ScrapyField, print_time
from .items import VideoItem

logger = logging.getLogger(__name__)


class SpiderProgressLogging(object):
    """
    周期性打印爬虫总进度
    """
    def __init__(self, stats):
        self.start_time = time.time()
        self.stats = stats
        self.settings = get_project_settings()

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # instantiate the extension object
        ext = cls(crawler.stats)  # 使extension可以访问stat

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed,
                                signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("爬虫启动：{}".format(spider.name))
        self.start_time = time.time()

    def spider_closed(self, spider):
        logger.info("爬虫关闭：{}".format(spider.name))
        print_time("爬取所用时间：", time.time() - self.start_time)

    def item_scraped(self, item, spider):
        if isinstance(item, VideoItem):
            self.stats.inc_value(ScrapyField.VideoCur.value)
            self.stats.set_value(ScrapyField.VideoTotal.value, spider.items_total)

            items_scraped = self.stats.get_value(ScrapyField.VideoCur.value)
            if items_scraped % 500 == 0:
                total_seconds = math.ceil(
                    (spider.items_total - items_scraped) / self.
                    settings['PER_PAGE']) * self.settings['DOWNLOAD_DELAY']
                hours = int(total_seconds // 3600)
                minutes = int(total_seconds % 3600 // 60)
                seconds = int(total_seconds % 3600 % 60)
                logger.info("总爬取进度：({}/{})，{:.1f}%，预计剩余时间 {}时{}分{}秒".format(
                    items_scraped,
                    spider.items_total,
                    items_scraped / spider.items_total * 100,
                    hours,
                    minutes,
                    seconds,
                ))


class _LoopingExtension:
    def setup_looping_task(self, task, crawler, interval):
        self._interval = interval
        self._task = LoopingCall(task)
        crawler.signals.connect(self.spider_opened,
                                signal=signals.spider_opened)
        crawler.signals.connect(self.spider_closed,
                                signal=signals.spider_closed)

    def spider_opened(self):
        self._task.start(self._interval, now=False)

    def spider_closed(self):
        if self._task.running:
            self._task.stop()


class DumpStatsExtension(_LoopingExtension):
    """
    周期性地将Stats数据写入日志
    """
    def __init__(self, crawler, interval):
        self.stats = crawler.stats
        self.setup_looping_task(self.print_stats, crawler, interval)

    def print_stats(self):
        stats = self.stats.get_stats()
        logger.info("Scrapy stats:\n" + pprint.pformat(stats))

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat("DUMP_STATS_INTERVAL")
        return cls(crawler, interval)
