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
            log_ch.setLevel(log_level)

            # 创建文件（.log）
            str_log_file = ('%s\\files\\study.log' % self.str_path)
            log_file = logging.FileHandler(filename=str_log_file, encoding='utf-8')

            # 创建格式
            log_format = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(name)s %(levelname)s %(message)s')

            # 添加格式
            log_ch.setFormatter(log_format)
            log_file.setFormatter(log_format)

            # 生成日志
            log_obj.addHandler(log_ch)
            log_obj.addHandler(log_file)

        return log_obj


def main():
    log_obj = Log().log_print()
    log_obj.debug('10：详细信息，调试问题')
    log_obj.info('20：确认事情按预期工作')
    log_obj.warning('30：发生意外，不影响目前工作')
    log_obj.error('40：产生错误，无法执行某些功能')
    log_obj.critical('50：严重错误，导致程序无法运行')

if __name__ == '__main__':
    main()
