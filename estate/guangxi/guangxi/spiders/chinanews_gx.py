# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class ChinanewGxSpider(CrawlSpider):

    name = 'chinanews_gx'
    allowed_domains = ['www.chinanews.com', 'sou.chinanews.com']

    def __init__(self):

        # http://sou.chinanews.com/search.do?q=%E5%B9%BF%E8%A5%BF&ps=100&time_scope=90&channel=estate&sort=pubtime&adv=1&day1=&day2=&field=&direction=&pager=0


        self.start_urls = (
            'http://sou.chinanews.com/search.do?q=%E5%B9%BF%E8%A5%BF&ps=100&time_scope=90&channel=estate&sort=pubtime&adv=1&day1=&day2=&field=&direction=&pager=0',
        )

        #http://www.chinanews.com/house/2015/11-03/7603161.shtml
        self.rules = (
            Rule(LinkExtractor(allow=('/house/\d{4}/\d{2}-\d{2}/\d{7}\.shtml',)), callback='parse_page'),
        )

        super(ChinanewGxSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://www.chinanews.com/house/'):

            year = url.split('/')[-3]
            month_day = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(year+month_day, '%Y%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

