# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class XkhouseNnSpider(CrawlSpider):

    name = 'xkhouse_nn'
    allowed_domains = ['news.nn.xkhouse.com',]

    def __init__(self):

        # http://news.nn.xkhouse.com/list157/?page=1
        self.start_urls = (
            'http://news.nn.xkhouse.com/list157/?page={}'.format(page) for page in range(1, 40)
        )

        # http://news.nn.xkhouse.com/html/2354128.html
        self.rules = (
            Rule(LinkExtractor(allow=('/html/\d{7}\.html',)), callback='parse_page'),
        )

        super(XkhouseNnSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://news.nn.xkhouse.com/html/'):

            date = response.css('.cont>.times::text').extract_first()

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item