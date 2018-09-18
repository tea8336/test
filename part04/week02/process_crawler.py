# coding:utf-8
# process_crawler.py
# yang.wenbo


import os
import requests
import random
import string

from concurrent.futures import ProcessPoolExecutor
from deco_time import DecoTime

STR_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STR_DOWNLOAD_DIR = os.path.join(STR_BASE_DIR, 'files')
LIST_URLS = ['https://source.unsplash.com/random', 'https://source.unsplash.com/user/erondu/1600x900']


class CrawlerProcess:

    def __init__(self):
        pass

    @DecoTime()
    def process_crawler(self):
        with ProcessPoolExecutor() as executor_obj:
            executor_obj.map(self.process_crawler_download, LIST_URLS)

    def process_crawler_download(self, str_url):
        response_obj = requests.get(str_url).content
        if response_obj:
            str_file_name = os.path.join(STR_DOWNLOAD_DIR, self.make_temp_name('.jpg'))
            self.crawler_save(str_file_name, response_obj)

    def crawler_save(self, str_file_name, obj_data):
        with open(str_file_name, 'wb') as file_obj:
            file_obj.write(obj_data)

    def make_temp_name(self, str_file_type):
        return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)]) + str_file_type


def main():
    CrawlerProcess().process_crawler()

if __name__ == '__main__':
    main()
