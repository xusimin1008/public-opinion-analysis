# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class SinaBeihaiSpider(CrawlSpider):

    name = 'sina_beihai'
    allowed_domains = ['beihai.house.sina.com.cn',]

    def __init__(self):

        # url_format = 'http://liuzhou.house.sina.com.cn/oldnews/{}.shtml'

        # start_date = datetime(year=2015, month=10, day=31)
        # end_date  = datetime(year=2015, month=7, day=1)
        # delta_date = timedelta(days=1)

        # date_list = []
        # while start_date >= end_date:
        #     date_list.append(start_date.strftime('%Y-%m-%d'))
        #     start_date -= delta_date

        self.start_urls = (
            'http://beihai.house.sina.com.cn/news/dongtai/',
        )

        #news/2015-10-27/06126064397931149325643.shtml
        self.rules = (
            Rule(LinkExtractor(allow=('/news/\d{4}-\d{2}-\d{2}/\d+\.shtml',)), callback='parse_page'),
        )

        super(SinaBeihaiSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://beihai.house.sina.com.cn/'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

