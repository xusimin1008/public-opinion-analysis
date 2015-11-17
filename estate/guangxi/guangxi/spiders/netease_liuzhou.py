# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class NeteaseLiuzhouSpider(CrawlSpider):

    name = 'netease_liuzhou'
    allowed_domains = ['liuzhou.house.163.com',]

    def __init__(self):


        first_url = ['http://liuzhou.house.163.com/special/03250MHC/hdhg.html', ]
        urls = [ 'http://liuzhou.house.163.com/special/03250MHC/hdhg_{:02}.html'.format(page) for page in range(2, 21) ]

        self.start_urls = first_url + urls

        # http://liuzhou.house.163.com/15/0624/08/ASS5HP8J032512QS.html
        self.rules = (
            Rule(LinkExtractor(allow=('/\d{2}/\d{4}/\d{2}/.+\.html',)), callback='parse_page'),
        )

        super(NeteaseLiuzhouSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://liuzhou.house.163.com/'):

            url_info = url.split('/')

            year = url_info[3]
            month_day = url_info[4]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(year+month_day, '%y%m%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

