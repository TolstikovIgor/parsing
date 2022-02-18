# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    user_id = scrapy.Field()
    photo = scrapy.Field()
    username = scrapy.Field()
    fullname = scrapy.Field()
    node = scrapy.Field()
    subscriptions = scrapy.Field()
    _id = scrapy.Field()

    pass
