import requests
import redis

from bs4 import BeautifulSoup
from datetime import datetime


class Download:
    '下载类'

    def __init__(self, dict_header=None, int_retries=3, int_delay=2, int_timeout=30):
        '''【初始化】
        dict_header：标头
        int_retries：重试
        delay：延迟
        timeout：超时'''
        self.dict_header = dict_header
        self.int_retries = int_retries
        self.int_delay = int_delay
        self.int_timeout = int_timeout

    def download_all(self, str_url):
        '''【下载页面】
        str_url：地址
        bool_json：是否json类型'''
        try:
            response_obj = requests.get(str_url, headers=self.dict_header, timeout=self.int_timeout)
            if response_obj.status_code == 200:
                return response_obj.content
        except Exception as e:
            str_html = ''
        return str_html


class Crawler:
    '爬虫类'

    def __init__(self, dict_header=None, int_retries=3, int_delay=2, int_timeout=30):
        '''【初始化】
        dict_header：标头
        int_retries：重试
        delay：延迟
        timeout：超时'''
        self.dict_header = dict_header
        self.int_retries = int_retries
        self.int_delay = int_delay
        self.int_timeout = int_timeout
        self.download = Download(dict_header, int_retries, int_delay, int_timeout)
        self.redis = Redis()

    def crawler_operate(self, str_url, int_page_start, int_page_end, int_page_step):
        str_date = ''
        int_page_num = 1
        for int_page in range(int_page_start, int_page_end, int_page_step):
            str_date += self.crawler_data(str_url.format(int_page))
            print('第%i页'.center(30, '*') % int_page_num)
            int_page_num += 1
        self.redis.redis_save(str_date)

    def crawler_data(self, str_url):
        '【处理数据】，str_url：地址'
        str_page = self.download.download_all(str_url)
        # 解析内容
        soup_obj = BeautifulSoup(str_page, 'lxml')
        soup_all_items = soup_obj.find_all('div', attrs={'class': 't_l_bd'})
        str_date = ''
        for soup_item in soup_all_items:
            # print('='*30)
            str_en = soup_item.find('p', attrs={'class': 't_l_en'}).find('a').text
            str_cn = soup_item.find('p', attrs={'class': 't_l_cn'}).find('a').text
            str_date += ('{}{}_'.format(str_en, str_cn))
        return str_date

    # def crawler_re_chars(self, str_text):
    #     '【过滤特殊符号】，str_text：文本'
    #     return re.sub('[^\u4e00-\u9fa5a-zA-Z0-9\'\",.，。!@#$%&*()]', '', str_text)


class Redis:

    def __init__(self, str_host='127.0.0.1', int_port=6379):
        '【初始化】'
        self.obj_clinet = redis.StrictRedis(str_host, int_port)

    def redis_save(self, str_value):
        '【记录】'
        self.obj_clinet.set(datetime.now().strftime("%Y%m%d%H%M"), str_value)

    def redis_query(self, str_key, str_count):
        '【查询】'
        try:
            list_value = self.obj_clinet.get(str_key).decode().split('_')
            for i in range(0, int(str_count)):
                print(list_value[i])
        except Exception as e:
            return 0


def main():
    # 地址
    str_url = 'http://news.iciba.com/appv3/wwwroot/ds.php?action=tags&id=4&ob=1&order=2&page={}'

    # 标头
    dict_header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'referer': 'http://my.iciba.com/index.php'
    }
    # 实例化
    crawler_obj = Crawler(dict_header=dict_header)
    # 获取3页数据
    # crawler_obj.crawler_operate(str_url, 1, 4, 1)
    Redis().redis_query('201810272251', 6)

if __name__ == '__main__':
    main()
