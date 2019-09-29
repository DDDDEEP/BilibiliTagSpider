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
    pubdate = Field()
    duration = Field()
    tags = Field()
    updated_at = Field()

    view = Field()
    danmaku = Field()
    reply = Field()
    favorite = Field()
    coin = Field()
    share = Field()
    like = Field()
    dislike = Field()


class TagItem(Item):
    collection = 'tags'

    _id = Field()
    tid = Field()
    tag_name = Field()


class TagVideoItem(Item):
    collection = 'tag_video'

    _id = Field()
    tid = Field()
    pubdate = Field()
    tag_id = Field()
    aid = Field()
