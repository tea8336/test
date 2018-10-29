# coding:utf-8
# redis_server.py
# yang.wenbo


import os
import sys
import redis
import socket

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
STR_CHECK_DT = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'{}\';'

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

    def mysql_add_author(self, str_name, str_city):
        '【添加作者】'
        Log().log_print().info('mysql_add_author...')
        try:
            model_author = Model_Authors()
            model_author.name = str_name
            model_author.city = str_city
            self.obj_session.add(model_author)
            self.obj_session.commit()
            print('添加作者成功')
        except Exception as e:
            Log().log_print().warning('添加作者失败')

    def mysql_add_article(self, str_title, int_author_id, str_content, str_comment):
        '【添加文章】'
        Log().log_print().info('mysql_add_article...')
        try:
            model_article = Model_Articles()
            model_article.title = str_title
            model_article.author_id = int_author_id
            model_article.content = str_content
            model_article.comment = str_comment
            self.obj_session.add(model_article)
            self.obj_session.commit()
            print('添加文章成功')
        except Exception as e:
            Log().log_print().warning('添加文章失败')

    def mysql_del_author(self, int_author_id):
        '【删除作者】'
        Log().log_print().info('mysql_del_author...')
        try:
            self.obj_session.query(Model_Authors).filter(Model_Authors.author_id == int_author_id).delete()
            self.obj_session.query(Model_Articles).filter(Model_Articles.author_id == int_author_id).delete()
            self.obj_session.commit()
            print('删除作者成功')
        except Exception as e:
            Log().log_print().warning('删除作者失败')

    def mysql_del_article(self, int_article_id):
        '【删除文章】'
        Log().log_print().info('mysql_del_article...')
        try:
            self.obj_session.query(Model_Articles).filter(Model_Articles.article_id == int_article_id).delete()
            self.obj_session.commit()
            print('删除文章成功')
        except Exception as e:
            Log().log_print().warning('删除文章失败')

    def mysql_show_authors(self):
        '【查询全部作者】'
        Log().log_print().info('mysql_show_author...')
        return self.obj_session.query(Model_Authors).all()

    def mysql_show_articles(self):
        '【查询全部文章】'
        Log().log_print().info('mysql_show_article...')
        return self.obj_session.query(Model_Articles, Model_Authors).join(Model_Authors, Model_Articles.author_id == Model_Authors.author_id).all()

    def mysql_select_author_by_id(self, int_author_id):
        '【根据作者ID查询作者】'
        Log().log_print().info('mysql_select_author_by_id...')
        return self.obj_session.query(Model_Authors).filter(Model_Authors.author_id == int_author_id).all()

    def mysql_select_article_by_id(self, int_article_id):
        '【根据文章ID查询文章】'
        Log().log_print().info('mysql_select_article_by_id...')
        return self.obj_session.query(Model_Articles, Model_Authors).join(Model_Authors, Model_Articles.author_id == Model_Authors.author_id).filter(Model_Articles.article_id == int_article_id).all()


class Operate_Ctl:

    def __init__(self):
        '【初始化】'
        Log().log_print().info('init Operate_Ctl...')
        self.obj_mysql = Operate_MySQL()
        self.list_authors = []
        self.list_articles = []
        self.obj_redis = Operate_Redis()

    def ctl_add_author(self):
        '【添加作者】'
        Log().log_print().info('ctl_add_author')
        str_author_name = self.ctl_input_check_len('请输入作者名称（最多50个字，【q】键取消）：', 51)
        if str_author_name.lower() == 'q':
            return
        str_author_city = self.ctl_input_check_len('请输入作者城市（最多20个字，【q】键取消）：', 21)
        if str_author_city.lower() == 'q':
            return
        self.obj_mysql.mysql_add_author(str_author_name, str_author_city)
        self.list_authors = self.obj_mysql.mysql_show_authors()

    def ctl_add_article(self):
        '【添加文章】'
        Log().log_print().info('ctl_add_article')
        str_article_title = self.ctl_input_check_len('请输入文章标题（最多20个字，【q】键取消）：', 21)
        if str_article_title.lower() == 'q':
            return
        self.ctl_show_authors()
        str_author_id = self.ctl_input_check_id('请输入作者编号（【q】键取消）:', 0)
        if str_author_id.lower() == 'q':
            return
        str_article_content = self.ctl_input_check_len('请输入文章内容（最多180个字，【q】键取消）:', 181)
        if str_article_content.lower() == 'q':
            return
        str_article_comment = self.ctl_input_check_len('请是输入评论（最多50个字，【q】键取消）:', 51)
        if str_article_comment.lower() == 'q':
            return
        self.obj_mysql.mysql_add_article(str_article_title, int(str_author_id), str_article_content, str_article_comment)
        self.list_articles = self.obj_mysql.mysql_show_articles()
        # TODO 发布文章
        str_author_name = self.obj_mysql.mysql_select_author_by_id(str_author_id)[0].name
        str_new_article = '书名：《{}》\n作者：{}\n内容：{}\n评论：{}'.format(str_article_title, str_author_name, str_article_content, str_article_comment)
        self.obj_redis.redis_publish(str_author_id, str_new_article)

    def ctl_del_author(self):
        '【删除作者】'
        Log().log_print().info('ctl_del_author')
        self.ctl_show_authors()
        str_author_id = self.ctl_input_check_id('请输入作者编号（同时将删除该作者的全部文章，【q】键取消）：', 0)
        if str_author_id.lower() == 'q':
            return
        self.obj_mysql.mysql_del_author(int(str_author_id))

    def ctl_del_article(self):
        '【删除文章】'
        Log().log_print().info('ctl_del_article')
        self.ctl_show_articles()
        str_article_id = self.ctl_input_check_id('请输入文章编号（【q】键取消）：', 1)
        if str_article_id.lower() == 'q':
            return
        self.obj_mysql.mysql_del_article(int(str_article_id))

    def ctl_show_authors(self):
        '【查询全部作者】'
        Log().log_print().info('ctl_show_authors')
        self.list_authors = self.obj_mysql.mysql_show_authors()
        for model_author in self.list_authors:
            print('{}.姓名：{}|城市：{}'.format(model_author.author_id, model_author.name, model_author.city))

    def ctl_show_articles(self):
        '【查询全部文章】'
        Log().log_print().info('ctl_show_articles')
        self.list_articles = self.obj_mysql.mysql_show_articles()
        for model_article in self.list_articles:
            print('{}.《{}》\n作者：{}\n内容：{}\n评论：{}\n创建时间：{}'.format(model_article[0].article_id, model_article[0].title, model_article[1].name, model_article[0].content, model_article[0].comment, model_article[0].create_date))

    def ctl_input_check_len(self, str_info, int_len):
        '【输入限制长度内容的文本】'
        Log().log_print().info('ctl_input_check_len')
        str_return = ''
        while True:
            str_return = input(str_info)
            if len(str_return) < int_len:
                break
        return str_return

    def ctl_input_check_id(self, str_info, int_type):
        '【输入操作的ID】：0-作者表，1-文章表'
        Log().log_print().info('ctl_input_check_len')
        str_return = ''
        while True:
            str_return = input(str_info)
            list_select = []
            if int_type == 0:
                list_select = self.obj_mysql.mysql_select_author_by_id(int(str_return))
            elif int_type == 1:
                list_select = self.obj_mysql.mysql_select_article_by_id(int(str_return))
            else:
                pass
            if len(list_select) > 0:
                break
        return str_return

    def ctl_show_traffic(self, str_article_id):
        '【查询文章访问量】'
        Log().log_print().info('ctl_show_traffic...')
        str_traffic = self.obj_redis.redis_query('article/{}'.format(str_article_id))
        print('article/{}访问量：{}'.format(str_article_id, str_traffic))


class Operate_Redis:

    def __init__(self, str_host='127.0.0.1', int_port=6379):
        '【初始化】'
        Log().log_print().info('init Operate_Redis...')
        self.obj_clinet = redis.StrictRedis(str_host, int_port)

    def redis_count(self, str_page):
        '【记录访问量】'
        Log().log_print().info('redis_count...')
        self.obj_clinet.incr(str_page)

    def redis_query(self, str_page):
        '【查询访问量】'
        Log().log_print().info('redis_query...')
        try:
            return int(self.obj_clinet.get(str_page))
        except Exception as e:
            return 0

    def redis_publish(self, str_author_id, str_new_article):
        '【发布文章】'
        Log().log_print().info('redis_publish...')
        self.obj_clinet.publish(str_author_id, str_new_article)


class Operate_HTTPServer:

    def __init__(self, str_host='127.0.0.1', int_port=8888, int_buffer_size=1024):
        '''【初始化】
        str_host：访问设置：localhost（本机）、IP值（IP）、空（任意主机）
        int_port：端口
        tuple_addr：地址(str_host, int_port)
        int_bsize_size：缓存（B）'''
        Log().log_print().info('init Operate_HTTPServer...')
        self.str_host = str_host
        self.int_port = int_port
        self.tuple_addr = (str_host, int_port)
        self.int_buffer_size = int_buffer_size
        self.obj_redis = Operate_Redis()

    def server_start(self):
        '【开启】'
        Log().log_print().info('server_start...')
        # 新建socket
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP-SOCK_STREAM，UDP-SOCK_DGRAM
        # 绑定地址
        socket_obj.bind(self.tuple_addr)
        # 监听连接的数量
        socket_obj.listen(1)
        # 启动服务，循环发送、接收数据
        print('启动HTTP服务')
        while True:
            # 等待连接
            print('等待连接...')
            socket_conn_obj, tuple_conn_addr = socket_obj.accept()
            print('成功连接：', tuple_conn_addr)
            # 接收数据
            data_obj = socket_conn_obj.recv(self.int_buffer_size)
            # print('收到数据：', data_obj)
            if data_obj:
                # 收到数据第一行：GET / HTTP/1.1
                # 收到数据第一行：GET /article/{all/article_id} HTTP/1.1
                request_path = data_obj.decode('utf-8').splitlines()[0]
                str_method, str_path, str_http = request_path.split()
                print('切换URL地址到：', str_path)
                str_response = ''
                # 页面输出
                list_path = str_path.split('/')
                if len(list_path) == 3 and list_path[1] == 'article':
                    dict_json = self.server_select_article(list_path[2])
                    str_response = self.server_show_jsonpage(dict_json)
                elif str_path == '/':
                    str_response = self.server_show_homepage()
                else:
                    str_response = self.server_show_errorpage()
                socket_conn_obj.sendall(str(str_response).encode('gbk'))
            else:
                pass
            socket_conn_obj.close()

    def server_select_article(self, str_article_id):
        '【查找文章数据】'
        Log().log_print().info('server_select_article...')
        dict_article = {'status': 0}
        list_articles = []
        try:
            if str_article_id == 'all':
                list_articles = Operate_MySQL().mysql_show_articles()
                dict_article['message'] = 'all articles'
            else:
                list_articles = Operate_MySQL().mysql_select_article_by_id(int(str_article_id))
                dict_article['message'] = 'No.{} article'.format(str_article_id)
                if len(list_articles) > 0:
                    self.obj_redis.redis_count('article/{}'.format(str_article_id))
            dict_article['articles'] = []
            for model_article in list_articles:
                dict_article['articles'].append({
                    'id': model_article[0].article_id,
                    'article': model_article[0].title,
                    'author': model_article[1].name,
                    'content': model_article[0].content})
            return dict_article
        except Exception as e:
            Log().log_print().warning(e)
            dict_article = {'status': 1, 'message': 'error', 'articles': []}
            return dict_article

    def server_show_jsonpage(self, dict_json):
        '【json页面】'
        Log().log_print().info('server_show_jsonpage...')
        return (f'''HTTP/1.1 200 OK

        <h1>Hello World</h1>
        {dict_json}''')

    def server_show_homepage(self):
        '【欢迎页面】'
        Log().log_print().info('server_show_homepage...')
        return '''HTTP/1.1 200 OK

        <h1>Hello World</h1>'''

    def server_show_errorpage(self):
        '【error页面】'
        Log().log_print().info('server_show_errorpage...')
        return '''HTTP/1.1 200 OK

        <h1>404</h1>'''


def help():
    '【命令提示】'
    print('帮助'.center(30, '='))
    dict_argvs = {
        '1.添加作者': '-aau --add_author',
        '2.添加文章': '-aar --add_article',
        '3.删除作者': '-dau --delete_author',
        '4.删除文章': '-dar --delete_article',
        '5.显示全部作者': '-sau --show_author',
        '6.显示全部文章': '-sar --show_article',
        '7.查询文章访问量': '-t {article_id} --traffic_article {article_id}'
    }
    for str_k in sorted(dict_argvs.keys()):
        print(f'{str_k}：{dict_argvs[str_k]}')


def main():
    try:
        if Engine.connect().execute(STR_CHECK_DT.format('authors')).fetchone() == None:
            Base.metadata.create_all()
            Log().log_print().info('创建数据表：authors、articles')
        if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
            help()
        elif len(sys.argv) == 2 and sys.argv[1] in ['-aau', '--add_author']:
            Operate_Ctl().ctl_add_author()
        elif len(sys.argv) == 2 and sys.argv[1] in ['-aar', '--add_article']:
            Operate_Ctl().ctl_add_article()
        elif len(sys.argv) == 2 and sys.argv[1] in ['-dau', '--delete_author']:
            Operate_Ctl().ctl_del_author()
        elif len(sys.argv) == 2 and sys.argv[1] in ['-dar', '--delete_article']:
            Operate_Ctl().ctl_del_article()
        elif len(sys.argv) == 2 and sys.argv[1] in ['-sau', '--show_author']:
            Operate_Ctl().ctl_show_authors()
        elif len(sys.argv) == 2 and sys.argv[1] in ['-sar', '--show_article']:
            Operate_Ctl().ctl_show_articles()
        elif len(sys.argv) == 3 and sys.argv[1] in ['-t', '--traffic_article']:
            Operate_Ctl().ctl_show_traffic(sys.argv[2])
        elif len(sys.argv) == 1:
            Operate_HTTPServer().server_start()
        else:
            print('没有这个命令')
            help()
    except Exception as e:
        Log().log_print().warning(e)


if __name__ == '__main__':
    main()
