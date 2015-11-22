# coding: utf-8

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json

from guangxi.models import db_session
from guangxi.models import db_model


# 房价
TOPIC1 = 1

# 开发商资金链
TOPIC2 = 1 << 1

# 降息
TOPIC3 = 1 << 2

# 土地市场
TOPIC4 = 1 << 3

# 公积金新政
TOPIC5 = 1 << 4

# 不动产登记
TOPIC6 = 1 << 5

# 旧城改造
TOPIC7 = 1 << 6

# 房产税改革
TOPIC8 = 1 << 7

# 保障性住房
TOPIC9 = 1 << 8

# 房地产成交量
TOPIC10 = 1 << 9


def check_topic1(word_freq):
    if (u"房产" in word_freq or u"楼市" in word_freq or u"房地产" in word_freq) and u"价格" in word_freq:
        return True
    return False

def check_topic2(word_freq):
    if u"开发商" in word_freq and u"资金链" in word_freq:
        return True
    return False

def check_topic3(word_freq):
    if u"降息" in word_freq or u"利率" in word_freq:
        return True
    return False

def check_topic4(word_freq):
    if (u"土地" in word_freq or u"地块" in word_freq) and ( u"市场" in word_freq or u"价格" in word_freq or u"地价" in word_freq ):
        return True
    return False

def check_topic5(word_freq):
    if u"住房贷款" in word_freq or u"公积金" in word_freq or u"首付" in word_freq:
        return True
    return False

def check_topic6(word_freq):
    if u"不动产" in word_freq and (u"不动产权" in word_freq or u"登记" in word_freq):
        return True
    return False

def check_topic7(word_freq):
    if u"棚户区" in word_freq or u"回迁房" in word_freq or ( u"旧城" in word_freq and u"改造" in word_freq):
        return True
    return False

def check_topic8(word_freq):
    if u"房产税" in word_freq and u"改革" in word_freq:
        return True
    return False

def check_topic9(word_freq):
    if u"公租房" in word_freq or ( u"保障性" in word_freq and u"住房" in word_freq ) or u"保障房" in word_freq:
        return True
    return False

def check_topic10(word_freq):
    if (u"资金" in word_freq or u"成交量" in word_freq or u"成交" in word_freq) and (u"房产" in word_freq or u"土地" in word_freq or u"地产" in word_freq or u"房地产" in word_freq):
        return True
    return False


def mark_topic():

    DB = 'mysql+pymysql://homestead:secret@127.0.0.1/public_opinion?charset=utf8'

    session = db_session(DB)
    M = db_model(DB, 'corpus')

    query = session.query(M)

    while True:
        corpuses = query.filter(M.status == 'segmented').order_by(M.id)
        if not corpuses:
            break

        for corpus in corpuses:
            try:
                word_freq = json.loads(corpus.word_freq)

                topic = 0

                if check_topic1(word_freq):
                    topic = topic | TOPIC1

                if check_topic2(word_freq):
                    topic = topic | TOPIC2

                if check_topic3(word_freq):
                    topic = topic | TOPIC3

                if check_topic4(word_freq):
                    topic = topic | TOPIC4

                if check_topic5(word_freq):
                    topic = topic | TOPIC5

                if check_topic6(word_freq):
                    topic = topic | TOPIC6

                if check_topic7(word_freq):
                    topic = topic | TOPIC7

                if check_topic8(word_freq):
                    topic = topic | TOPIC8

                if check_topic9(word_freq):
                    topic = topic | TOPIC9

                if check_topic10(word_freq):
                    topic = topic | TOPIC10

                corpus.topic = topic
                session.commit()

                print('===> mark topic, id: ', corpus.id)

            except:
                print('===> mark topic error, id: ', corpus.id)

            corpus.status = 'marked'
            session.commit()


if __name__ == '__main__':
    mark_topic()

