# coding: utf-8

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from readability.readability import Document

from bs4 import BeautifulSoup as BS

from guangxi.models import db_session
from guangxi.models import db_model

def extract_content():

    DB = 'mysql+pymysql://homestead:secret@127.0.0.1/public_opinion?charset=utf8'

    session = db_session(DB)
    M = db_model(DB, 'corpus')

    query = session.query(M)

    while True:
        corpuses = query.filter(M.status == 'ready').order_by(M.id).limit(30).all()
        if not corpuses:
            break

        for corpus in corpuses:
            try:
                summary_html = Document(corpus.html).summary(html_partial=True)
                content = BS(summary_html).text.strip()
                corpus.content = content
                session.commit()
            except:
                corpus.content = '[extract_error]'
                session.commit()
                print('===> extract_content error, id: ', corpus.id)

            corpus.status = 'extracted'
            session.commit()

if __name__ == '__main__':
    extract_content()