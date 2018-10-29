# coding:utf-8
# rabbitmq_client.py
# yang.wenbo


import sys
import uuid
import pika

from rabbitmq_base import Rabbitmq_Base
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
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


class Model_Articles(Base):
    __tablename__ = 'articles'
    # ID、文章标题、作者ID、内容、评论、创建日期
    article_id = Column('article_id', Integer, primary_key=True)
    title = Column('title', String(20), nullable=False)
    author_id = Column('author_id', Integer)
    content = Column('content', String(180))
    comment = Column('comment', String(50))
    create_date = Column('create_date', DateTime, default=datetime.now())


class Operate_MySQL:

    def __init__(self):
        '【初始化】'
        Log().log_print().info('init Operate_MySQL...')
        self.obj_session = Session()

    def mysql_show_articles(self):
        '【查询全部文章】'
        Log().log_print().info('mysql_show_article...')
        list_articles = self.obj_session.query(Model_Articles, Model_Authors).join(Model_Authors, Model_Articles.author_id == Model_Authors.author_id).all()
        for model_article in list_articles:
            print('{}.《{}》\n作者：{}\n内容：{}\n评论：{}\n创建时间：{}'.format(model_article[0].article_id, model_article[0].title, model_article[1].name, model_article[0].content, model_article[0].comment, model_article[0].create_date))
        return list_articles


class Operate_RabbitMQ(Rabbitmq_Base):
    
    def __init__(self):
        '【初始化】'
        Log().log_print().info('init Operate_RabbitMQ...')
        super().__init__()
        self.obj_result = None
        self.str_queue_name = self.make_random_queue()
        self.str_corr_id = str(uuid.uuid4())
        self.obj_channel.basic_consume(self.callback, queue=self.str_queue_name, no_ack=True)

    def callback(self, obj_channel, obj_method, obj_properties, obj_body):
        '【callback】'
        Log().log_print().info('callback...')
        # print('callback id: ', self.str_corr_id)
        if self.str_corr_id == obj_properties.correlation_id:
            self.obj_result = obj_body

    def call(self, r):
        '【call】'
        Log().log_print().info('call...')
        self.obj_channel.basic_publish(exchange='', routing_key="study", body=str(r), properties=pika.BasicProperties(reply_to=self.str_queue_name, correlation_id=self.str_corr_id))
        while self.obj_result is None:
            print('正在等待...')
            self.obj_connection.process_data_events(10)
        return self.obj_result


def check_id(str_info, list_articles):
        '【输入操作的ID】'
        Log().log_print().info('check_id')
        str_return = ''
        while True:
            str_return = input(str_info)
            if str_return.lower() == 'q':
                return str_return
            for obj_article in list_articles:
                if int(str_return) == obj_article[0].article_id:
                    return str_return


def main():
    obj_rabbitmq = Operate_RabbitMQ()
    str_article_id = ''
    str_article = ''
    if len(sys.argv) == 2:
        str_article_id = sys.argv[1]
        str_article = obj_rabbitmq.call(str_article_id).decode('utf-8')
    else:
        list_articles = Operate_MySQL().mysql_show_articles()
        if len(list_articles) > 0:
            str_article_id = check_id('请输入文章编号（【q】键取消）：', list_articles)
            if str_article_id.lower() == 'q':
                return
            str_article = obj_rabbitmq.call(str_article_id).decode('utf-8')
    print(str_article)


if __name__ == '__main__':
    main()
