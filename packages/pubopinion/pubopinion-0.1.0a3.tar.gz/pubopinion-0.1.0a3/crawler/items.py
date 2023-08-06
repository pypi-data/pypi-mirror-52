# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PublicOpinionCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HTMLItem(scrapy.Item):
    url = scrapy.Field()
    text = scrapy.Field()


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
    datetime = scrapy.Field()


class QQNewsItem(scrapy.Item):
    meta = scrapy.Field()


class QQNewsJRYWItem(scrapy.Item):
    pass