# coding:utf-8
# process_crawler_url.py
# yang.wenbo


import os
import re
import sys
import random
import string
import requests

from multiprocessing import Process, Pool
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from concurrent.futures import ProcessPoolExecutor
from deco_time import DecoTime
from log import Log

STR_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STR_DOWNLOAD_DIR = os.path.join(STR_BASE_DIR, 'files')
# LIST_URLS = ['https://www.baidu.com', 'https://www.163.com/']


class CrawlerProcess:

    def __init__(self):
        Log().log_print().info('init CrawlerProcess...')
        pass

    @DecoTime()
    def process_crawler(self, str_url):
        Log().log_print().info('process_crawler...')
        with ProcessPoolExecutor() as executor_obj:
            Log().log_print().info('process_crawler_download_start...')
            executor_obj.map(self.process_crawler_download, str_url)
        Log().log_print().info('process_crawler_download_end...')

    def process_crawler_download(self, str_url):
        '【抓取数据】'
        # 下载
        try:
            response_obj = requests.get(str_url).text
        except RequestException as e:
            print(e)
        # 筛选
        soup_obj = BeautifulSoup(response_obj, 'lxml')
        str_as = soup_obj.find_all('a')
        str_hrefs = ''
        for str_href in str_as:
            if str(str_href.get('href'))[:4] == 'http':
                str_hrefs += '%s\n' % str_href.get('href')
        # 保存
        if len(str_hrefs.strip()) > 0:
            Log().log_print().info('{}'.format(str_hrefs))
            str_file_name = os.path.join(STR_DOWNLOAD_DIR, self.make_temp_name('.txt'))
            self.crawler_save(str_file_name, str_hrefs, str_url)

    def crawler_save(self, str_file_name, obj_data, str_url):
        '【保存】'
        Log().log_print().info('crawler_save...')
        with open(str_file_name, 'w', encoding='utf-8') as file_obj:
            file_obj.write(obj_data)

    def make_temp_name(self, str_file_type):
        '【随机生成文件名】'
        Log().log_print().info('make_temp_name...')
        return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)]) + str_file_type


def help():
    '【命令提示】'
    print('帮助'.center(30, '='))
    dict_argvs = {
        '帮助': '-h --help', 
        '爬虫': '-c url（如：https://www.baidu.com） --crawler url（如：https://www.baidu.com）'
    }
    for str_k in sorted(dict_argvs.keys()):
        print(f'{str_k}：{dict_argvs[str_k]}')
    str_input = input('按【q】键退出，其他任意键继续：').lower()
    if str_input == 'q':
        print('谢谢使用')
        return
    else:
        start()


def check_url(str_url):
    '【验证url】'
    re_url = re.compile('^(https?|ftp|file)://.+$')
    if re_url.match(str_url) == None:
        return False
    else:
        return True


def crawler():
    '【启动】'
    str_url = input('请输入URL（如：https://www.baidu.com）：')
    while check_url(str_url) == False:
        str_url = input('请输入正确的URL（如：https://www.baidu.com）：')
    CrawlerProcess().process_crawler([str_url])
    str_input = input('按【q】键退出，其他任意键继续：').lower()
    if str_input == 'q':
        print('谢谢使用')
        return
    else:
        crawler()


def start():
    dict_type = {'1': '爬虫', '2': '帮助', '3': '退出'}
    for str_k in sorted(dict_type.keys()):
        print(f'{str_k}：{dict_type[str_k]}')
    str_input = input('请选择操作：')
    if str_input == '1':
        crawler()
    elif str_input == '2':
        help()
    elif str_input == '3':
        print('谢谢使用')
        return
    else:
        print('没有这个操作')
        start()


def main():
    try:
        if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
            help()
            return
        elif len(sys.argv) == 3 and sys.argv[1] in ['-c', '--crawler']:
            if check_url(sys.argv[2]) == False:
                print('{}不是正确的URL（如：https://www.baidu.com）'.format(sys.argv[2]))
            else:
                CrawlerProcess().process_crawler([sys.argv[2]])
            return
        else:
            start()
    except Exception as e:
        print(e)
        

if __name__ == '__main__':
    main()
