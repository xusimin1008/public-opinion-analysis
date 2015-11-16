# coding: utf-8

from datetime import datetime

from grab.spider import Spider
from grab.spider import Task

import logging
logging.basicConfig(level=logging.DEBUG)


class FangNnSpider(Spider):
    '''
    http://news.nn.fang.com

    url: http://news.nn.fang.com/news/gdxw/2015-11-13/1.html
    url
    '''

    def task_generator(self):

        url_format = 'http://news.nn.fang.com/news/gdxw/{}/{}.html'
        now_date = datetime.now().strftime('%Y-%m-%d')
        #for page in range(1, 51):
        for page in range(1, 3):
            url = url_format.format(now_date, page)
            yield Task('list', url=url)

        for lang in ('python', 'ruby', 'perl'):
            url = 'https://www.google.com/search?q=%s' % lang
            yield Task('search', url=url, lang=lang)


    def task_list(self, grab, task):
        logging.info()

    # def task_search(self, grab, task):
    #     print('%s: %s' % (task.lang,
    #                       grab.doc('//div[@class="s"]//cite').text()))


if __name__ == '__main__':

    spider = FangNnSpider()
    spider.run()