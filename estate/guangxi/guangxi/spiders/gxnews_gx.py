# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class GxnewsGxSpider(CrawlSpider):

    name = 'gxnews_gx'
    allowed_domains = ['house.gxnews.com.cn',]

    def __init__(self):

        # http://house.gxnews.com.cn/staticmores/607/24607-10.shtml
        self.start_urls = (
            'http://house.gxnews.com.cn/staticmores/607/24607-{}.shtml'.format(page) for page in range(1, 70)
        )

        # http://house.gxnews.com.cn/staticpages/20150701/newgx55931a0c-13094008.shtml
        self.rules = (
            Rule(LinkExtractor(allow=('/staticpages/\d{8}/newgx\w+-\d{8}\.shtml',)), callback='parse_page'),
        )

        super(GxnewsGxSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://house.gxnews.com.cn/staticpages/'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y%m%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

