# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class LoupanNnSpider(CrawlSpider):

    name = 'loupan_nn'
    allowed_domains = ['nn.loupan.com',]

    def __init__(self):

        # 
        self.start_urls = (
            'http://nn.loupan.com/news/list-36-{}.html'.format(page) for page in range(1, 39)
        )

        # http://nn.loupan.com/html/news/201506/1847327.html
        self.rules = (
            Rule(LinkExtractor(allow=('/html/news/\d{6}/\d{7}\.html',)), callback='parse_page'),
        )

        super(LoupanNnSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://nn.loupan.com/html/news/'):

            date = response.css('p.time-form::text').extract_first().split()[0]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date.encode('utf-8'), '%Y年%m月%d日')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

