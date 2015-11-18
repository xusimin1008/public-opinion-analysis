# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class GxfdcGxSpider(CrawlSpider):

    name = 'gxfdc_gx'
    allowed_domains = ['news.gxfdc.cn',]

    def __init__(self):

        # 
        self.start_urls = (
            'http://news.gxfdc.cn/News/NewsChildList.aspx?ClassID=4&page={}'.format(page) for page in range(1, 2)
        )

        # http://news.gxfdc.cn/News/News4_410294.shtml
        self.rules = (
            Rule(LinkExtractor(allow=('/News/News4_\d{6}.shtml',)), callback='parse_page'),
        )

        super(GxfdcGxSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://news.gxfdc.cn/News/'):

            date = response.css('div.newstitle_down div::text').extract()[1].split()[-1][-10:]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

