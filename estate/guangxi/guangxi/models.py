# coding: utf-8

# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.automap import automap_base

# global
engine = None


def db_engine(db_url):
    global engine
    if not engine:
        engine = create_engine(db_url)
    return engine


def db_session(db_url):
    engine = db_engine(db_url) 
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    return session


def db_model(db_url, table_name):
    engine = db_engine(db_url)
    db_base = automap_base()
    db_base.prepare(engine, reflect=True)
    model = db_base.classes.get(table_name)
    return model


if __name__ == '__main__':
    from IPython import embed
    
    DB_URL = 'mysql+pymysql://homestead:secret@127.0.0.1/public_opinion'

    session = db_session(DB_URL)
    M = db_model(DB_URL, 'corpus')

    # session.add(M(url='test_url', status='test_status'))
    # session.commit()

    query = session.query(M)
    r = query.filter(M.url == 'test_url').first()

    embed()

