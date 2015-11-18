# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class QqLiuzhouSpider(CrawlSpider):

    name = 'qq_liuzhou'
    allowed_domains = ['liuzhou.house.qq.com',]

    def __init__(self):

        first_page = ['http://liuzhou.house.qq.com/l/news/qgxw/list2012127111235.htm',]
        other_pages = ['http://liuzhou.house.qq.com/l/news/qgxw/list2012127111235_{}.htm'.format(page) for page in range(2, 6)]
        self.start_urls = first_page + other_pages

        # http://liuzhou.house.qq.com/a/20150716/015079.htm
        self.rules = (
            Rule(LinkExtractor(allow=('/a/\d{8}/\d{6}\.htm',)), callback='parse_page'),
        )

        super(QqLiuzhouSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://liuzhou.house.qq.com/a'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y%m%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item