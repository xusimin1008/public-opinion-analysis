# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class Zp365FcgSpider(CrawlSpider):

    name = 'zp365_fcg'
    allowed_domains = ['fcg.zp365.com',]

    def __init__(self):

        # 
        self.start_urls = (
            'http://fcg.zp365.com/News/NewsChildList.aspx?ClassID=412',
            'http://fcg.zp365.com/News/NewsChildList.aspx?ClassID=414',
        )

        # http://fcg.zp365.com/News/News414_422126.shtml
        self.rules = (
            Rule(LinkExtractor(allow=('/News/News\d{3}_\d{6}\.shtml',)), callback='parse_page'),
        )

        super(Zp365FcgSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://fcg.zp365.com/News/'):

            date = response.css('div.newstitle_down div[style="float:left;"]::text').extract()[-1].split()[-1]

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date.encode('utf-8'), '时间：%Y-%m-%d')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

