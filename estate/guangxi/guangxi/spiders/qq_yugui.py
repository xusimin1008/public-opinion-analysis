# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class QqYuguiSpider(CrawlSpider):

    name = 'qq_yugui'
    allowed_domains = ['yugui.house.qq.com',]

    def __init__(self):

        self.start_urls = ['http://yugui.house.qq.com/newslist/lpdg.htm', ]

        # http://yugui.house.qq.com/a/20150827/093100.htm
        self.rules = (
            Rule(LinkExtractor(allow=('/a/\d{8}/\d{6}\.htm',)), callback='parse_page'),
        )

        super(QqYuguiSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://yugui.house.qq.com/a'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y%m%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item