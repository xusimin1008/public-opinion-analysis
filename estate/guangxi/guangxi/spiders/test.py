# -*- coding: utf-8 -*-
import scrapy


class TestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = scrapy.Field()


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = []
    start_urls = (
        'http://httpbin.org/get' for i in range(10)
    )

    def parse(self, response):
        
        item = TestItem()
        item['content'] = response.body_as_unicode()

        return item
