import sqlsoup
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Engine(object):
    def __new__(cls, connect_url):
        engine = create_engine(connect_url,
                               strategy='threadlocal',
                               pool_size=5,
                               pool_recycle=1800,
                               encoding='utf-8',
                               max_overflow=2)
        return engine


class DB(object):
    def __new__(cls, connect_url):
        return sqlsoup.SQLSoup(Engine(connect_url), session=scoped_session(sessionmaker(
            autoflush=False,
            expire_on_commit=False,
            autocommit=True)))


if __name__ == '__main__':
    # db = DB('mysql://root:123456@localhost:3306/test?charset=utf8')
    pass
