# coding:utf-8
# log.py
# yang.wenbo


import os
import logging


class Log:
    '日志类'

    def __init__(self):
        '【初始化】'
        self.str_path = os.path.dirname(os.path.abspath(__file__))
        # # 关闭日志
        # logging.disable(logging.CRITICAL)

    def log_print(self, str_log_name: str = 'study-log', log_level: int = logging.DEBUG):

        # 创建对象
        log_obj = logging.getLogger(str_log_name)
        log_obj.setLevel(log_level)

        # 判断handlers是否已经添加过
        if not log_obj.handlers:

            # 创建控制台
            log_ch = logging.StreamHandler()
            log_ch.setLevel(logging.WARNING)

            # 创建文件（.log）
            str_log_file = ('%s\\files\\study.log' % self.str_path)
            log_file = logging.FileHandler(filename=str_log_file, encoding='utf-8')
            log_file.setLevel(logging.DEBUG)

            # 创建格式
            log_format = logging.Formatter('%(levelname)-10s: %(message)s')

            # 添加格式
            log_ch.setFormatter(log_format)
            log_file.setFormatter(log_format)

            # 生成日志
            log_obj.addHandler(log_ch)
            log_obj.addHandler(log_file)

        return log_obj
