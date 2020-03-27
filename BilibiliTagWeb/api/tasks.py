from __future__ import absolute_import, unicode_literals
import os
import time
import threading

from celery import current_task, shared_task
from celery_once import QueueOnce
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from BilibiliTagHandler.tag_handler import TagHandler
from BilibiliTagSpider.spiders.TagSpider import TagSpider
from BilibiliTagWeb import settings
from helpers import *

def handler_start(handler, type_id, time_from, time_to_end):
    return handler.start(type_id, time_from, time_to_end)

@shared_task(base = QueueOnce)
def task_handler(type_id, time_from, time_to_end):
    mongo_settings = settings.DATABASES['default']
    handler = TagHandler(mongo_settings['HOST'],
                        mongo_settings['NAME'],
                        mongo_settings['USER'],
                        mongo_settings['PASSWORD']) 
    thread_handler = ThreadWithReturnValue(
        target = handler_start,
        args = (handler, type_id, time_from, time_to_end)
    )
    thread_handler.start()
    while True:
        current_task.update_state(
            # state = 'PROGRESS',
            meta = {
                'status': HandlerErrcode.Running,
                'handle_count': handler.handle_count,
                'handle_total': handler.handle_total,
                'calculate_count': handler.calculate_count,
                'calculate_total': handler.calculate_total,
            }
        )
        time.sleep(1)
        if not thread_handler.is_alive():
            break

    return {
        'status': thread_handler.get_return(),
        'handle_count': handler.handle_count,
        'handle_total': handler.handle_total,
        'calculate_count': handler.calculate_count,
        'calculate_total': handler.calculate_total,
    }


def spider_crawl(process, crawler, type_id, time_from, time_to_end):
    process.crawl(crawler, type_id=type_id, time_from=20160101, time_to=20160101)
    process.start()

@shared_task(base = QueueOnce)
def task_spider(type_id, time_from, time_to_end):
    settings = Settings()
    settings_module_path = os.environ.get('SCRAPY_ENV', 'BilibiliTagSpider.settings')   
    settings.setmodule(settings_module_path, priority='project')
    process = CrawlerProcess(settings=settings)
    crawler = process.create_crawler(TagSpider)

    thread_spider = Thread(
        target = spider_crawl,
        args = (process, crawler, type_id, time_from, time_to_end)
    )
    thread_spider.start()
    while True:
        current_task.update_state(
            # state = 'PROGRESS',
            meta = {
                'video_item_cur': crawler.stats.get_value(SCRAPY_STAT_VIDEO_CUR),
                'video_item_total': crawler.stats.get_value(SCRAPY_STAT_VIDEO_TOTAL),
            }
        )
        time.sleep(1)
        if not thread_spider.is_alive():
            break

    return {
        'video_item_cur': crawler.stats.get_value(SCRAPY_STAT_VIDEO_CUR),
        'video_item_total': crawler.stats.get_value(SCRAPY_STAT_VIDEO_TOTAL),
    }