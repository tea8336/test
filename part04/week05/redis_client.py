# coding:utf-8
# redis_client.py
# yang.wenbo


import redis

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from log import Log


STR_HOST = '127.0.0.1'
STR_PORT = '3306'
STR_USER = 'root'
STR_PWD = 'admin'
STR_DB = 'study'

STR_DBURL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'

Engine = create_engine(STR_DBURL.format(STR_USER, STR_PWD, STR_HOST, STR_PORT, STR_DB))
Base = declarative_base(Engine)
Session = sessionmaker(Engine)


class Model_Authors(Base):
    __tablename__ = 'authors'
    # ID、作者姓名、城市
    author_id = Column('author_id', Integer, primary_key=True)
    name = Column('name', String(50), nullable=False)
    city = Column('city', String(20))


class Operate_MySQL:

    def __init__(self):
        '【初始化】'
        Log().log_print().info('init Operate_MySQL...')
        self.obj_session = Session()

    def mysql_all_authors_id(self):
        '【查询全部作者】'
        Log().log_print().info('mysql_show_author...')
        obj_authors = self.obj_session.query(Model_Authors).all()
        list_authors = [obj_author.author_id for obj_author in obj_authors]
        return list_authors


class Operate_Redis:

    def __init__(self, str_host='127.0.0.1', int_port=6379):
        '【初始化】'
        Log().log_print().info('init Operate_Redis...')
        self.obj_clinet = redis.StrictRedis(str_host, int_port)
        self.list_authors = Operate_MySQL().mysql_all_authors_id()

    def redis_subscribe(self):
        '【订阅文章】'
        Log().log_print().info('redis_subscribe...')
        obj_subscribe = self.obj_clinet.pubsub()
        obj_subscribe.subscribe(self.list_authors)
        self.redis_show('publish_all', obj_subscribe)

    def redis_show(self, str_name, obj_subscribe):
        '【显示订阅】'
        Log().log_print().info('redis_show...')
        for obj_msg in obj_subscribe.listen():
            # print(obj_msg)
            if obj_msg["type"] == "message":
                print(obj_msg['data'].decode())
            pass


def main():
    print('显示订阅...')
    Operate_Redis().redis_subscribe()

if __name__ == '__main__':
    main()
