# coding:utf-8
# thread_crawler.py
# yang.wenbo


import os
import random
import string
import asyncio
import aiohttp

from deco_time import DecoTime

STR_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STR_DOWNLOAD_DIR = os.path.join(STR_BASE_DIR, 'files')
LIST_URLS = ['https://source.unsplash.com/random', 'https://source.unsplash.com/user/erondu/1600x900']


class CrawlerThread:

    def __init__(self):
        pass

    @DecoTime()
    def async_crawler(self):
        async_loop = asyncio.get_event_loop()
        async_loop.run_until_complete(self.async_crawler_start(async_loop))

    async def async_crawler_start(self, async_loop):
        list_tasks = [self.async_crawler_download(str_url, async_loop) for str_url in LIST_URLS]
        await asyncio.gather(*list_tasks)

    async def async_crawler_download(self, str_url, async_loop):
        async with aiohttp.ClientSession(loop=async_loop) as aio_session:
            async with aio_session.get(str_url) as session_obj:
                str_file_name = os.path.join(STR_DOWNLOAD_DIR, self.make_temp_name('.jpg'))
                with open(str_file_name, 'wb') as file_obj:
                    while True:
                        session_obj_read = await session_obj.content.read(1024)
                        if not session_obj_read:
                            break
                        file_obj.write(session_obj_read)

    def make_temp_name(self, str_file_type):
        return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)]) + str_file_type


def main():
    CrawlerThread().async_crawler()

if __name__ == '__main__':
    main()
