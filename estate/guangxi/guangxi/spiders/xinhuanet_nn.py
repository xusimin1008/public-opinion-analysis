# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class XinhuanetNnSpider(CrawlSpider):

    name = 'xinhuanet_nn'
    allowed_domains = ['news.xinhuanet.com', 'search.news.cn']

    def __init__(self):

        self.start_urls = (
            'http://search.news.cn/mb/xinhuanet/search/?nodetype=3&nodeid=1189545&styleurl=http://www.xinhuanet.com/local/static/style/css_erji.css',
            'http://search.news.cn/mb/xinhuanet/search/?nodetype=3&nodeid=1189551&styleurl=http://www.xinhuanet.com/local/static/style/css_erji.css',
        )

        #http://news.xinhuanet.com/house/nn/2015-10-28/c_1116962036.htm
        self.rules = (
            Rule(LinkExtractor(allow=('/house/nn/\d{4}-\d{2}-\d{2}/c_\d{10}.htm',)), callback='parse_page'),
        )

        super(XinhuanetNnSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://news.xinhuanet.com/house/'):

            date = url.split('/')[-2]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

