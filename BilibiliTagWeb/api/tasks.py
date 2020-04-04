from __future__ import absolute_import, unicode_literals
import os
import time
from threading import Thread

from celery import current_task, shared_task
from celery_once import QueueOnce
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from api.models import Tasks
from BilibiliTagHandler.tag_handler import TagHandler
from BilibiliTagSpider.spiders.TagSpider import TagSpider
from BilibiliTagWeb import settings
from helpers import ThreadWithReturnValue, HandlerErrcode, ScrapyField, HandlerField


def task_ended(task_id):
    """记录数据库中对应的task记录完成"""
    task = Tasks.objects.get(task_id=task_id)
    task.time_end = int(time.time())
    task.save()


def handler_start(handler, type_id, time_from, time_to):
    return handler.start(type_id, time_from, time_to)


@shared_task(base=QueueOnce, bind=True)
def task_handler(self, type_id, time_from, time_to):
    mongo_settings = settings.DATABASES['default']
    handler = TagHandler(mongo_settings['HOST'], mongo_settings['NAME'],
                         mongo_settings['USER'], mongo_settings['PASSWORD'])
    thread_handler = ThreadWithReturnValue(target=handler_start,
                                           args=(handler, type_id, time_from,
                                                 time_to))
    thread_handler.start()
    while True:
        current_task.update_state(state='PROGRESS',
                                  meta={
                                      HandlerField.Status.value:
                                      HandlerErrcode.Running.value,
                                      HandlerField.HandleCur.value:
                                      handler.handle_cur,
                                      HandlerField.HandleTotal.value:
                                      handler.handle_total,
                                      HandlerField.CalCur.value:
                                      handler.calculate_cur,
                                      HandlerField.CalTotal.value:
                                      handler.calculate_total,
                                  })
        time.sleep(1)
        if not thread_handler.is_alive():
            break

    task_ended(self.request.id)
    return {
        HandlerField.Status.value: thread_handler.get_return(),
        HandlerField.HandleCur.value: handler.handle_cur,
        HandlerField.HandleTotal.value: handler.handle_total,
        HandlerField.CalCur.value: handler.calculate_cur,
        HandlerField.CalTotal.value: handler.calculate_total,
    }


def spider_crawl(process, crawler, type_id, time_from, time_to):
    process.crawl(crawler,
                  type_id=type_id,
                  time_from=time_from,
                  time_to=time_to)
    process.start(stop_after_crawl=False)


@shared_task(base=QueueOnce, bind=True)
def task_spider(self, type_id, time_from, time_to):
    settings = Settings()
    settings_module_path = os.environ.get('SCRAPY_ENV',
                                          'BilibiliTagSpider.settings')
    settings.setmodule(settings_module_path, priority='project')
    process = CrawlerProcess(settings=settings)
    crawler = process.create_crawler(TagSpider)

    thread_spider = Thread(target=spider_crawl,
                           args=(process, crawler, type_id, time_from,
                                 time_to))
    thread_spider.start()

    video_cur = 0
    video_total = 0
    while True:
        if (crawler.stats.get_value(ScrapyField.VideoCur.value) is None or \
                crawler.stats.get_value(ScrapyField.VideoTotal.value) is None):
            continue
        video_cur = crawler.stats.get_value(ScrapyField.VideoCur.value)
        video_total = crawler.stats.get_value(ScrapyField.VideoTotal.value)
        current_task.update_state(state='PROGRESS',
                                  meta={
                                      ScrapyField.VideoCur.value: video_cur,
                                      ScrapyField.VideoTotal.value:
                                      video_total,
                                  })
        time.sleep(1)
        # 线程有时候不会释放，还是从业务逻辑上跳出循环
        if video_cur == video_total:
            break

    task_ended(self.request.id)
    return {
        ScrapyField.VideoCur.value:
        crawler.stats.get_value(ScrapyField.VideoCur.value),
        ScrapyField.VideoTotal.value:
        crawler.stats.get_value(ScrapyField.VideoTotal.value),
    }