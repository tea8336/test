# coding:utf-8
# celery_client.py
# yang.wenbo


import redis


class Redis:

    def __init__(self, str_host='127.0.0.1', int_port=6379):
        '【初始化】'
        self.obj_clinet = redis.StrictRedis(str_host, int_port)

    def redis_query(self, str_key, str_count):
        '【查询】'
        try:
            list_value = self.obj_clinet.get(str_key).decode().split('_')
            for i in range(0, int(str_count)):
                print(list_value[i])
        except Exception as e:
            print('没有查询数据')


def main():
    print('欢迎使用'.center(30, '='))
    while True:
        str_key = input('请输入查询时间，格式年月日时分（如：201810272257），按【q】键退出：')
        if str_key.lower() == 'q':
            return
        while True:
            str_num = input('请输入显示数量，按【q】键退出：')
            if str_num.lower() == 'q':
                return
            if str_num.isdigit() == True:
                break
        Redis().redis_query(str_key, str_num)


if __name__ == '__main__':
    main()
