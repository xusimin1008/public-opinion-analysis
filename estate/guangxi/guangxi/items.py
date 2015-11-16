# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class PageItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     url = scrapy.Field()
#     test_info = scrapy.Field()


class CorpusItem(scrapy.Item):

    url = scrapy.Field()
    website = scrapy.Field()
    published_at = scrapy.Field()
    html = scrapy.Field()
    status = scrapy.Field()
