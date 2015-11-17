# coding: utf-8

from datetime import datetime
from datetime import timedelta

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class FangGuigangSpider(CrawlSpider):

    name = 'fang_guigang'
    allowed_domains = ['news.guigang.fang.com',]

    def __init__(self):

        url_format = 'http://news.guigang.fang.com/news/gdxw/{}/{}.html'

        start_date = datetime(year=2015, month=10, day=31)
        end_date  = datetime(year=2015, month=7, day=1)
        delta_date = timedelta(days=1)

        date_list = []
        while start_date >= end_date:
            date_list.append(start_date.strftime('%Y-%m-%d'))
            start_date -= delta_date

        self.start_urls = (
            url_format.format(date, 1) for date in date_list
        )

        self.rules = (
            Rule(LinkExtractor(allow=('/\d{4}-\d{2}-\d{2}/\d{8}\.htm',)), callback='parse_page'),
        )

        super(FangGuigangSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://news.guigang.fang.com'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

