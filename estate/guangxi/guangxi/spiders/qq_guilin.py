# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class QqGuilinSpider(CrawlSpider):

    name = 'qq_guilin'
    allowed_domains = ['guilin.house.qq.com',]

    def __init__(self):

        first_page = ['http://guilin.house.qq.com/l/news/hydt/list_hydt.htm',]
        other_pages = ['http://guilin.house.qq.com/l/news/hydt/list_hydt_{}.htm'.format(page) for page in range(2, 30)]
        self.start_urls = first_page + other_pages

        # http://guilin.house.qq.com/a/20150916/023285.htm
        self.rules = (
            Rule(LinkExtractor(allow=('/a/\d{8}/\d{6}\.htm',)), callback='parse_page'),
        )

        super(QqGuilinSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://guilin.house.qq.com/a'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y%m%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item