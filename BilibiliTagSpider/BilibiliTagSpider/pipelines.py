# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from bson import ObjectId


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
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DB'),
                   mongo_usr=crawler.settings.get("MONGO_USR"),
                   mongo_pwd=crawler.settings.get("MONGO_PWD"),
                   )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            self.mongo_uri,
            username=self.mongo_usr,
            password=self.mongo_pwd
        )
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].update({'aid': item['aid']}, item, True)
        # item['_id'] = ObjectId()
        # self.db[item.collection].insert(item)
        return item

    def close_spider(self, spider):
        self.client.close()
