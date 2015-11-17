# coding: utf-8

from datetime import datetime
from datetime import timedelta

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class SinaLiuzhouSpider(CrawlSpider):

    name = 'sina_liuzhou'
    allowed_domains = ['liuzhou.house.sina.com.cn',]

    def __init__(self):
        #http://gx.house.sina.com.cn/oldnews/2015-11-16.shtml
        url_format = 'http://liuzhou.house.sina.com.cn/oldnews/{}.shtml'

        start_date = datetime(year=2015, month=10, day=31)
        end_date  = datetime(year=2015, month=7, day=1)
        delta_date = timedelta(days=1)

        date_list = []
        while start_date >= end_date:
            date_list.append(start_date.strftime('%Y-%m-%d'))
            start_date -= delta_date

        self.start_urls = (
            url_format.format(date) for date in date_list
        )

        #/scan/2015-11-16/09126071826984827409385.shtml
        self.rules = (
            Rule(LinkExtractor(allow=('/scan/\d{4}-\d{2}-\d{2}/\d+\.shtml',)), callback='parse_page'),
        )

        super(SinaLiuzhouSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://liuzhou.house.sina.com.cn/'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

