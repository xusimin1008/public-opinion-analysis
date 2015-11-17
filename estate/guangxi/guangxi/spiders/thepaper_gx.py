# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class ThepaperGxSpider(CrawlSpider):

    name = 'thepaper_gx'
    allowed_domains = ['www.thepaper.cn',]

    def __init__(self):

        # 通过搜索来检索
        self.start_urls = (
            'http://www.thepaper.cn/searchResult.jsp?inpsearch=%E5%B9%BF%E8%A5%BF+%E6%88%BF%E4%BA%A7',
        )

        #http://www.thepaper.cn/newsDetail_forward_1395709
        self.rules = (
            Rule(LinkExtractor(allow=('/newsDetail_forward_\d{7}',)), callback='parse_page'),
        )

        super(ThepaperGxSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://www.thepaper.cn/'):

            date = response.css('div.news_about > p:nth-child(2)::text').extract_first().split(' ')[0]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

