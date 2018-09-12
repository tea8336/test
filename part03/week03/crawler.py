# coding:utf-8
# crawler.py
# yang.wenbo


import os
import re
import csv
import json
import time
import requests
import log

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime, timedelta
from requests.exceptions import RequestException


class Valve:
    '阀门类'

    def __init__(self, int_delay: int=2):
        '【初始化】，int_delay：延迟'
        self.log = log.Log().log_print()
        self.log.info('初始化Valve类')
        self.int_delay = int_delay
        self.dict_domains = {}

    def valve_wait(self, str_url: str):
        '【延迟访问】，str_url：访问地址'
        str_domain = urlparse(str_url).netloc
        date_last_accessed = self.dict_domains.get(str_domain)
        if self.int_delay > 0 and date_last_accessed is not None:
            int_wait_second = self.int_delay - (datetime.now() - date_last_accessed).seconds
            if int_wait_second > 0:
                self.log.info('延迟访问%s' % str_url)
                time.sleep(int_wait_second)
        self.dict_domains[str_domain] = datetime.now()


class Recorder:
    '记录类'

    def __init__(self, str_fun_name: str = 'record_csv'):
        '【初始化】'
        self.log = log.Log().log_print()
        self.log.info('初始化Recorder类')
        self.str_fun_name = str_fun_name

    def __call__(self, str_file_name: str, tuple_items: tuple, list_all: list):
        '''【回调函数】
        str_file_name：文件名
        tuple_items：字段
        list_all：数据'''
        if hasattr(self, self.str_fun_name):
            fun_obj = getattr(self, self.str_fun_name)
            return fun_obj(str_file_name, tuple_items, list_all)
        else:
            self.log.info('没有记录方法')
            return {'status': 1, 'statusText': '没有记录方法'}

    def record_csv(self, str_file_name: str, tuple_items: tuple, list_all: list):
        '''【记录数据】
        str_file_name：文件名
        tuple_items：字段
        list_all：数据'''
        try:
            # Excel默认以ANSI格式编辑.csv文件，所以保存为ANSI格式，以避免乱码
            with open(str_file_name, 'w', newline='', encoding='ansi') as file_obj:
                write_obj = csv.writer(file_obj)
                write_obj.writerow(tuple_items)
                for tuple_row in list_all:
                    write_obj.writerow(tuple_row)
            self.log.info('记录成功')
            return {'status': 0, 'statusText': '记录成功'}
        except Exception as e:
            print(e)
            self.log.info('记录失败')
            return {'status': 1, 'statusText': '记录失败'}


class Download:
    '下载类'

    def __init__(self, dict_header: dict=None, int_retries: int=3, int_delay: int=2, int_timeout: int=30):
        '''【初始化】
        dict_header：标头
        int_retries：重试
        delay：延迟
        timeout：超时'''
        self.log = log.Log().log_print()
        self.log.info('初始化Download类')
        self.dict_header = dict_header
        self.int_retries = int_retries
        self.int_delay = int_delay
        self.int_timeout = int_timeout
        self.valve_obj = Valve(int_delay)

    def download_all(self, str_url: str, bool_json: bool):
        '''【下载页面】
        str_url：地址
        bool_json：是否json类型'''
        self.valve_obj.valve_wait(str_url)
        try:
            response_obj = requests.get(str_url, headers=self.dict_header, timeout=self.int_timeout)
            if response_obj.status_code == 200:
                if bool_json:
                    self.log.info('返回json类型')
                    return response_obj.json()
                else:
                    self.log.info('返回非json类型')
                    return response_obj.content
        except RequestException as e:
            str_html = ''
            if hasattr(e.response, 'status_code'):
                int_code = e.response.status_code
                print('error code: %i' % int_code)
                if self.int_retries > 0 and int_code > 499 and int_code < 600:
                    str_html = self.download(str_url)
                    self.int_retries -= 1
                else:
                    int_code = None
        return str_html


class Crawler:
    '爬虫类'

    def __init__(self, dict_header: dict=None, int_retries: int=3, int_delay: int=2, int_timeout: int=30):
        '''【初始化】
        dict_header：标头
        int_retries：重试
        delay：延迟
        timeout：超时'''
        self.log = log.Log().log_print()
        self.log.info('初始化Crawler类')
        self.dict_header = dict_header
        self.int_retries = int_retries
        self.int_delay = int_delay
        self.int_timeout = int_timeout
        self.download = Download(dict_header, int_retries, int_delay, int_timeout)

    def crawler_operate(self, str_url: str, int_page_start: int, int_page_end: int, int_page_step: int, str_file_name: str, callback=None):
        '''【爬虫操作】
        str_url：地址
        int_page_start：起始页
        int_page_end：结束页
        int_page_step：页码间隔
        str_file_name：文件名称
        callback：写入文件'''
        list_all = []
        int_page_num = 1
        for int_page in range(int_page_start, int_page_end, int_page_step):
            list_date = self.crawler_data(str_url.format(int_page))
            list_all += list_date
            self.log.info('第%i页'.center(30, '*') % int_page_num)
            int_page_num += 1

        if callback:
            callback(str_file_name, ('id', '名称', '价格', '评价人数', '好评率'), list_all)

    def crawler_data(self, str_url: str):
        '【处理数据】，str_url：地址'
        str_page = self.download.download_all(str_url, False)
        # 解析内容
        soup_obj = BeautifulSoup(str_page, 'lxml')
        soup_all_items = soup_obj.find_all('li', attrs={'class': 'gl-item'})
        self.log.info('商品总数：%i' % len(soup_all_items))

        list_data = []
        for soup_item in soup_all_items:
            self.log.info('='*30)
            str_thinkpad_id = soup_item['data-sku']
            # 商品名称过滤掉特殊符号
            str_thinkpad_name = self.crawler_re_chars(soup_item.find('div', attrs={'class': 'p-name'}).find('em').text)
            str_thinkpad_price = soup_item.find('div', attrs={'class': 'p-price'}).find('i').text
            str_thinkpad_url = ('https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1' % str_thinkpad_id)
            str_thinkpad_count, str_thinkpad_rate = self.crawler_item_evaluate(str_thinkpad_url)

            tuple_row = (str_thinkpad_id, str_thinkpad_name, str_thinkpad_price, str_thinkpad_count, str_thinkpad_rate)
            list_data.append(tuple_row)
            self.log.info(tuple_row)

        return list_data

    def crawler_item_evaluate(self, str_url: str):
        '【评价数据】，str_path：地址'
        item_data = self.download.download_all(str_url, True)
        return item_data['productCommentSummary']['commentCount'], item_data['productCommentSummary']['goodRate']

    def crawler_re_chars(self, str_text: str):
        '【过滤特殊符号】，str_text：文本'
        return re.sub('[^\u4e00-\u9fa5a-zA-Z0-9\'\",.，。!@#$%&*()]', '', str_text)


def main():
    # 地址
    str_url = 'https://search.jd.com/Search?keyword=ThinkPad&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=ThinkPad&page={}&s=62&click=0'
    # 标头
    dict_header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'referer': 'https://help.jd.com/index.html'
    }
    # 实例化
    crawler_obj = Crawler(dict_header=dict_header)
    # 获取3页数据
    str_path = os.path.dirname(os.path.abspath(__file__))
    crawler_obj.crawler_operate(str_url, 1, 6, 2, ('%s\\files\\study.csv' % str_path), Recorder('record_csv'))  

if __name__ == '__main__':
    main()
