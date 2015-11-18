# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class QqNnSpider(CrawlSpider):

    name = 'qq_nn'
    allowed_domains = ['nn.house.qq.com',]

    def __init__(self):

        # 
        self.start_urls = (
            'http://nn.house.qq.com/newslist/2013bdxw.htm',
            'http://nn.house.qq.com/newslist/2013gnxw.htm',
            'http://nn.house.qq.com/newslist/2013lpdt.htm',
            'http://nn.house.qq.com/newslist/2013lsdt.htm',
            'http://nn.house.qq.com/newslist/2013lpdg.htm',
            'http://nn.house.qq.com/newslist/2013zybd.htm',
            'http://nn.house.qq.com/newslist/2013tdzc.htm',
            'http://nn.house.qq.com/newslist/2013lssj.htm',
            'http://nn.house.qq.com/newslist/2013djxw.htm',
            'http://nn.house.qq.com/newslist/2013kftu.htm',
            'http://nn.house.qq.com/newslist/2013zjgd.htm',
            'http://nn.house.qq.com/newslist/2013rwmdm.htm',
        )

        # http://nn.house.qq.com/a/20151026/051376.htm
        self.rules = (
            Rule(LinkExtractor(allow=('/a/\d{8}/\d{6}.htm',)), callback='parse_page'),
        )

        super(QqNnSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://nn.house.qq.com/a/'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y%m%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

