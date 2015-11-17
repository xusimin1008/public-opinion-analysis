# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class FocusGlSpider(CrawlSpider):

    name = 'focus_gl'
    allowed_domains = ['news.focus.cn',]

    def __init__(self):

        # http://news.focus.cn/nn/yaowen/100/
        self.start_urls = (
            'http://news.focus.cn/gl/yaowen/{}/'.format(page) for page in range(1, 101)
        )

        # http://news.focus.cn/nn/2015-11-16/10525005.html
        self.rules = (
            Rule(LinkExtractor(allow=('/gl/\d{4}-\d{2}-\d{2}/\d{8}.html',)), callback='parse_page'),
        )

        super(FocusGlSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://news.focus.cn/gl/'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

