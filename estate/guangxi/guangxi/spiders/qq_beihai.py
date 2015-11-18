# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class QqBeihaiSpider(CrawlSpider):

    name = 'qq_beihai'
    allowed_domains = ['beihai.house.qq.com',]

    def __init__(self):

        self.start_urls = ['http://beihai.house.qq.com/list/bdxw.htm', ]

        # http://beihai.house.qq.com/a/20150918/019887.htm
        self.rules = (
            Rule(LinkExtractor(allow=('/a/\d{8}/\d{6}\.htm',)), callback='parse_page'),
        )

        super(QqBeihaiSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://beihai.house.qq.com/a'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y%m%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item