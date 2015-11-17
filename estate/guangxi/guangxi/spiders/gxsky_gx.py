# coding: utf-8

from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from guangxi.items import CorpusItem


class GxskyGxSpider(CrawlSpider):

    name = 'gxsky_gx'
    allowed_domains = ['bbs.gxsky.com', 'house.gxsky.com']

    def __init__(self):

        # http://bbs.gxsky.com/portal.php?mod=list&catid=539&page=1
        self.start_urls = (
            'http://bbs.gxsky.com/portal.php?mod=list&catid=539&page={}'.format(page) for page in range(1, 4)
        )

        # http://house.gxsky.com/article-439444-1.html
        self.rules = (
            Rule(LinkExtractor(allow=('/article-\d{6}-\d\.html',)), callback='parse_page'),
        )

        super(GxskyGxSpider, self).__init__()

    def parse_page(self, response):

        url = response.url
        if url.startswith('http://house.gxsky.com/'):

            date = response.css('#left_news > div.left_news_nr_title > h2::text').extract()[1].strip()

            item = CorpusItem()
            item['url'] = url
            item['website'] = self.name
            item['published_at'] = datetime.strptime(date, '%Y-%m-%d %H:%M')
            item['html'] = response.body_as_unicode()
            item['status'] = 'ready'

            return item

