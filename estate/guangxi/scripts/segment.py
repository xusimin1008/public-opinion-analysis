# coding: utf-8

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import re
from collections import Counter

import jieba

from guangxi.models import db_session
from guangxi.models import db_model


accepted_token_patten = re.compile(ur"[\u4E00-\u9FA5]{2,}")

cur_path = os.path.dirname(os.path.abspath(__file__))
stop_words_file_path = os.path.join(cur_path, 'stop_words.txt')
userdict_file_path = os.path.join(cur_path, 'custom_words.txt')
jieba.load_userdict(userdict_file_path)


def load_stop_words():
    stop_words = []
    with open(stop_words_file_path, 'r') as f:
        lines = f.readlines()
        stop_words = [line.decode('utf-8').strip() for line in lines]
    return stop_words

stop_words = load_stop_words()


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def token_condition(t):
    if not accepted_token_patten.match(t):
        return False

    if t in stop_words:
        return False

    return True


def segment_text(raw_text):

    tokens = jieba.tokenize(raw_text)
    seg_list = [w for (w, start_pos, stop_pos) in tokens if token_condition(w)]

    seg_freq_counter = Counter(seg_list)
    seg_freq = dict(seg_freq_counter)

    return json.dumps(seg_freq)


def segment():

    DB = 'mysql+pymysql://homestead:secret@127.0.0.1/public_opinion?charset=utf8'

    session = db_session(DB)
    M = db_model(DB, 'corpus')

    query = session.query(M)

    while True:
        corpuses = query.filter(M.status == 'extracted', M.content != '[extract_error]').order_by(M.id).limit(50).all()
        if not corpuses:
            break

        for corpus in corpuses:
            try:
                corpus.wrod_freq = segment_text(corpus.content)
                session.commit()
            except:
                print('===> segment error, id: ', corpus.id)

            corpus.status = 'segmented'
            session.commit()


if __name__ == '__main__':
    segment()