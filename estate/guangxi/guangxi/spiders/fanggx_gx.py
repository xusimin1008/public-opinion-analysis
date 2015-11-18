# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class FanggxGxSpider(CrawlSpider):

    name = 'fanggx_gx'
    allowed_domains = ['www.fanggx.com',]

    def __init__(self):

        # 
        self.start_urls = (
            'http://www.fanggx.com/gxi/news/loushikuaixun/{}.html'.format(page) for page in range(1, 6)
        )

        # http://www.fanggx.com/gxi/news/201505/659069/1.html
        self.rules = (
            Rule(LinkExtractor(allow=('/gxi/news/\d{6}/\d{6}/\d\.html',)), callback='parse_page'),
        )

        super(FanggxGxSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://www.fanggx.com/gxi/news/'):

            date = response.css('div.article-dfa::text').extract_first().split()[0]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item