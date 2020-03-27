# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class VideoItem(Item):
    collection = 'videos'

    _id = Field()
    aid = Field()
    tid = Field()
    title = Field()
    duration = Field()
    pubdate = Field()
    tags = Field()
    created_at = Field()
    updated_at = Field()

    stat_view = Field()
    stat_danmaku = Field()
    stat_reply = Field()
    stat_favorite = Field()
    stat_coin = Field()
    stat_share = Field()
    stat_like = Field()
    stat_dislike = Field()

class RecordItem(Item):
    collection = 'records'

    _id = Field()
    tid = Field()
    pubdate = Field()
    status = Field()
    created_at = Field()
    updated_at = Field()
