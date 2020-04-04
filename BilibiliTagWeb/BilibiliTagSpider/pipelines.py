# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from .items import RecordItem, VideoItem


class BilibilitagspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_usr, mongo_pwd):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_usr = mongo_usr
        self.mongo_pwd = mongo_pwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_usr=crawler.settings.get('MONGO_USR'),
            mongo_pwd=crawler.settings.get('MONGO_PWD'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri,
                                          username=self.mongo_usr,
                                          password=self.mongo_pwd)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if isinstance(item, VideoItem):
            self.db[item.collection].update_one({
                'aid': item['aid'],
            }, {
                '$setOnInsert': {
                    'created_at': item['created_at'],
                    'tid': item['tid'],
                    'pubdate': item['pubdate'],
                    'aid': item['aid'],
                    'tags': item['tags'],
                },
                '$set': {
                    'updated_at': item['updated_at'],
                    'title': item['title'],
                    'duration': item['duration'],
                    'stat_view': item['stat_view'],
                    'stat_danmaku': item['stat_danmaku'],
                    'stat_reply': item['stat_reply'],
                    'stat_favorite': item['stat_favorite'],
                    'stat_coin': item['stat_coin'],
                    'stat_share': item['stat_share'],
                    'stat_like': item['stat_like'],
                    'stat_dislike': item['stat_dislike'],
                }
            },
                                                upsert=True)
            return item
        elif isinstance(item, RecordItem):
            self.db[item.collection].update_one(
                {
                    'tid': item['tid'],
                    'pubdate': item['pubdate'],
                }, {'$set': {
                    'status': item['status'],
                }},
                upsert=True)

    def close_spider(self, spider):
        self.client.close()
