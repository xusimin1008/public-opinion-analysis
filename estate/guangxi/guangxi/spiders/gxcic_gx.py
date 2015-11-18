# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class GxcicGxSpider(CrawlSpider):

    name = 'gxcic_gx'
    allowed_domains = ['gxcic.net',]

    def __init__(self):

        # 
        self.start_urls = (
            'http://gxcic.net/news/newsclass.aspx?ClassID=2',
        )

        # http://gxcic.net/HTMLFile/2015-10/shownews_185107.html
        self.rules = (
            Rule(LinkExtractor(allow=('/HTMLFile/\d{4}-\d{2}/shownews_\d{6}\.html',)), callback='parse_page'),
        )

        super(GxcicGxSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://gxcic.net/HTMLFile/'):

            date = response.css('#Labeltitle2::text').extract_first().split(' ')[0]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y/%m/%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

