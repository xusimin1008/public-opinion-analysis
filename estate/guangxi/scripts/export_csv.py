# coding: utf-8

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import csv

from guangxi.models import db_session
from guangxi.models import db_model


csvfile_path = 'estate_corpus_guagnxi_20151120.csv'


def export_csv():

    DB = 'mysql+pymysql://homestead:secret@127.0.0.1/public_opinion?charset=utf8'

    session = db_session(DB)
    M = db_model(DB, 'corpus')

    query = session.query(M)

    csv_file = open(csvfile_path, 'wb')
    writer = csv.writer(csv_file)

    table_head = ['url', 'website', 'published_at', 'word_freq', 'topic']
    writer.writerow(table_head)


    offset = 0
    limit  = 3000

    while True:

        corpuses = query.filter(M.status == 'marked').order_by(M.id).offset(offset).limit(limit).all()

        if not corpuses:
            break

        for corpus in corpuses:
            table_row = [corpus.url, corpus.website, corpus.published_at, corpus.word_freq, corpus.topic]
            writer.writerow(table_row)
            print('===> write id: ', corpus.id)

        offset += limit

    csv_file.close()



if __name__ == '__main__':
    export_csv()