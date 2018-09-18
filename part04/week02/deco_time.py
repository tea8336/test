# coding:utf-8
# deco_time.py
# yang.wenbo


import time

from functools import wraps


class DecoTime:

    def __init__(self):
        pass

    def __call__(self, fun_obj):
        @wraps(fun_obj)
        def wrapper(*tuple_args, **dict_kwargs):
            print('开始运行{}...'.format(fun_obj.__name__))
            time_start = time.time()
            fun_obj(*tuple_args, **dict_kwargs)
            time_deco = time.time() - time_start
            print('运行{}共用时{}秒'.format(fun_obj.__name__, time_deco))
        return wrapper
