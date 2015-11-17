# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class IfengNnSpider(CrawlSpider):

    name = 'ifeng_nn'
    allowed_domains = ['nn.house.ifeng.com',]

    def __init__(self):

        # http://nn.house.ifeng.com/news/city/0
        self.start_urls = (
            'http://nn.house.ifeng.com/news/city/{}'.format(page) for page in range(30)
        )

        # http://nn.house.ifeng.com/detail/2014_03_06/1940773_0.shtml
        self.rules = (
            Rule(LinkExtractor(allow=('/detail/\d{4}_\d{2}_\d{2}/.+\.shtml',)), callback='parse_page'),
        )

        super(IfengNnSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://nn.house.ifeng.com/detail/'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y_%m_%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item