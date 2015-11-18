# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class ZhiyeNnSpider(CrawlSpider):

    name = 'zhiye_nn'
    allowed_domains = ['www.0771555.com',]

    def __init__(self):

        first_page = ['http://www.0771555.com/article/lsxw/']
        other_pages = ['http://www.0771555.com/article/lsxw/index{}.html'.format(page) for page in range(1, 4)]

        self.start_urls = first_page + other_pages

        # http://www.0771555.com/article/201506/1610.html
        self.rules = (
            Rule(LinkExtractor(allow=('/article/\d{6}/\d{4}\.html',)), callback='parse_page'),
        )

        super(ZhiyeNnSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://www.0771555.com/article/'):

            date = response.css('#content_writer td[width="150"]::text').extract_first()

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date.encode('utf-8'), '日期：%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item