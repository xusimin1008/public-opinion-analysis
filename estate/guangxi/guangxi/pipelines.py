# coding: utf-8

from guangxi.models import db_session, db_model
from guangxi.settings import DB


class CorpusPipeline(object):

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGO_URI'),
    #         mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
    #     )

    def open_spider(self, spider):
        self.session = session = db_session(DB)
        self.model = db_model(DB, 'corpus_test')
        self.query = self.session.query(self.model)

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):

        corpus = self.query.filter(self.model.url == item['url']).first()

        if corpus:
            spider.logger.info('===> already have this item')
            return item

        # 写入
        corpus = self.model(
            url=item['url'],
            website=item['website'],
            location='guangxi',
            published_at=item['published_at'],
            html=item['html'],
            status=item['status'],
        )
        self.session.add(corpus)
        self.session.commit()

        return item
