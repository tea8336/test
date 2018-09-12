# coding:utf-8
# decorator.py
# yang.wenbo


import os
import re
import sys
import json
import log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from functools import wraps
from week01 import word, excel, pdf
from week02 import img


STR_PATH = ('%s\\files' % os.path.dirname(os.path.abspath(__file__)))
STR_LOG = log.Log().log_print()


class Recorder:
    '记录类'

    def __init__(self):
        '【初始化】'
        log.Log().log_print().debug('Recorder-init')

    @staticmethod
    def recorder_json(str_path: str, str_username: str, str_password: str, str_type: str, list_auth: list, str_enable: str):
        '''【记录JSON】，保存用户信息到JSON文件
        str_path：文件名
        str_username：用户名
        str_password：密码
        str_type：用户类型
        list_auth：操作权限
        str_enable：账户状态'''
        try:
            log.Log().log_print().debug('recorder_json')
            dict_json = {
                'username': str_username,
                'password': str_password,
                'type': str_type,
                'auth': list_auth,
                'enable': str_enable
            }
            with open(str_path, 'w') as file_obj:
                json.dump(dict_json, file_obj)
            # print(json.dumps(dict_json, ensure_ascii=False))
            print('保存用户信息成功')
            log.Log().log_print().debug('保存用户信息成功')
        except Exception as e:
            log.Log().log_print().warning('保存用户信息失败')


class Reloader:
    '读取类'

    def __init__(self):
        '【初始化】'
        log.Log().log_print().debug('Reloader-init')

    @staticmethod
    def reloader_json(str_path: str):
        '【读取JSON】，读取JSON文件信息'
        try:
            log.Log().log_print().debug('reloader_json')
            dict_json = {}
            with open(str_path, 'r') as file_obj:
                dict_json = json.load(file_obj)
            # print(dict_json)
        except Exception as e:
            log.Log().log_print().warning('读取用户信息失败')
        finally:
            return dict_json


class Manage:
    '用户管理类'

    def __init__(self, str_fun_name: str):
        '【初始化】'
        self.str_log = log.Log().log_print()
        self.str_log.debug('Manage-init')
        self.str_fun_name = str_fun_name
        self.dict_user_info = {}

    def __call__(self, fun_obj: object):
        '【回调】'
        @wraps(fun_obj)
        def wrapper(*tuple_args):
            self.str_log.debug('Manage-call')
            if hasattr(self, self.str_fun_name):
                fun_manage = getattr(self, self.str_fun_name)
                if fun_manage(*tuple_args):
                    fun_obj(*tuple_args)
                    return self.dict_user_info
        return wrapper

    def check_user(self, *tuple_args):
        '''【登录】
        tuple_args[0]：用户名
        tuple_args[1]：密码
        返回：验证成功返回True，验证失败返回False'''
        self.str_log.debug('check_user')
        str_user_file = '%s\\%s.json' % (STR_PATH, tuple_args[0])
        if os.path.exists(str_user_file):
            self.dict_user_info = Reloader.reloader_json(str_user_file)
            if self.dict_user_info['password'] == tuple_args[1]:
                print('登录成功')
                self.str_log.debug('登录成功')
                return True
            else:
                print('用户名、密码不匹配，请重新登录')
                self.str_log.debug('用户名、密码不匹配，请重新登录')
                operate(login())
        else:
            str_bool_register = input('用户%s不存在，按【r】键注册，其它任意键退出：' % tuple_args[0]).lower()
            if str_bool_register == 'r':
                self.register(str_user_file, tuple_args[0])
                print('注册完毕，请重新登录')
                self.str_log.debug('注册完毕，请重新登录')
                operate(login())
            else:
                return False

    def register(self, str_user_file, str_username):
        '''【用户注册】
        str_user_file：用户JSON文件
        str_username：用户名'''
        self.str_log.debug('register')
        print('用户注册：%s'.center(30, '=') % str_username)
        str_password = input('请输入密码：')
        str_type = '1'
        list_auth = ["q"]
        str_enable = '0'
        # 写入JSON文件
        Recorder.recorder_json(str_user_file, str_username, str_password, str_type, list_auth, str_enable)

    @staticmethod
    def auth(str_user_file: str, str_update_username: str, dict_operate_type: dict):
        '【用户权限设置】'
        log.Log().log_print().debug('auth')
        print('设置用户权限'.center(30, '-'))
        list_auth = Manage.input_auth('请输入用户权限，可以多选（如1或12）：', dict_operate_type)
        dict_update_user = Reloader.reloader_json(str_user_file)
        # 写入JSON文件
        Recorder.recorder_json(str_user_file, dict_update_user['username'], dict_update_user['password'], dict_update_user['type'], list_auth, dict_update_user['enable'])
        print('权限设置成功，请重新登录生效')
        operate(login())

    @staticmethod
    def input_auth(str_input_info: str, dict_operate_type: dict):
        '【输入权限】'
        log.Log().log_print().debug('input_auth')
        for str_k in sorted(dict_operate_type.keys()):
            print('%s.%s' % (str_k, dict_operate_type[str_k]))
        str_input = input('请输入%s' % str_input_info)
        bool_return, list_return = Manage.check_auth(str_input, dict_operate_type)
        while bool_return == False:
            str_input = input('请重新输入正确的%s' % str_input_info)
            bool_return, list_return = Manage.check_auth(str_input, dict_operate_type)
        return list_return

    @staticmethod
    def check_auth(str_input: str, dict_operate_type: dict):
        '【验证权限】'
        log.Log().log_print().debug('check_auth')
        list_auth = []
        for int_index in range(len(str_input)):
            if not dict_operate_type.get(str_input[int_index]):
                return False, []
            else:
                list_auth.append(str_input[int_index])
        if 'q' not in list_auth:
            list_auth.append('q')
        return True, list_auth


class Operate:
    '操作类'

    def __init__(self, str_fun_name: str):
        '【初始化】'
        self.str_log = log.Log().log_print()
        self.str_log.debug('Operate-init')
        self.str_fun_name = str_fun_name
        self.dict_operate_type = {'0': '用户权限设置', '1': '图片', '2': 'Word', '3': 'Excel', '4': 'PDF', 'q': '退出'}
        self.dict_user_info = {}
        self.dict_json_files = {}

    def __call__(self, fun_obj: object):
        '【回调】'
        @wraps(fun_obj)
        def wrapper(*tuple_args):
            self.str_log.debug('Operate-call')
            if hasattr(self, self.str_fun_name):
                fun_manage = getattr(self, self.str_fun_name)
                if tuple_args[0] == None:
                    return
                if fun_manage(*tuple_args):
                    fun_obj(*tuple_args)
        return wrapper

    def start_operate(self, *tuple_args):
        '【操作】'
        self.str_log.debug('start_oprate')
        self.dict_user_info = tuple_args[0]
        print('您好%s，功能列表：'.center(30, '*') % self.dict_user_info['username'])
        dict_current_user_info = {}
        for str_operate in self.dict_user_info['auth']:
            dict_current_user_info[str_operate] = self.dict_operate_type[str_operate]
        # 操作
        str_operate = self.input_operate('操作编号：', dict_current_user_info)
        if str_operate == '0':
            self.str_log.debug('用户权限设置')
            self.auth_operate()
        elif str_operate == '1':
            self.str_log.debug('图片')
            img.main()
            self.start_operate(*tuple_args)
        elif str_operate == '2':
            self.str_log.debug('Word')
            word.main()
            self.start_operate(*tuple_args)
        elif str_operate == '3':
            self.str_log.debug('Excel')
            excel.main()
            self.start_operate(*tuple_args)
        elif str_operate == '4':
            self.str_log.debug('PDF')
            pdf.main()
            self.start_operate(*tuple_args)
        elif str_operate.lower() == 'q':
            self.str_log.debug('退出')
            return True
        else:
            pass

    def input_operate(self, str_input_info: str, dict_info: dict):
        '【输入操作类型】'
        self.str_log.debug('input_operate')
        print(str_input_info.center(30, '-'))
        for str_k in sorted(dict_info.keys()):
            print('%s.%s' % (str_k, dict_info[str_k]))
        str_input = input('请输入%s' % str_input_info)
        while dict_info.get(str_input) == None:
            str_input = input('请重新输入正确的%s' % str_input_info)
        return str_input

    def auth_operate(self):
        '【权限】'
        self.str_log.debug('auth_operate')
        list_users = os.listdir(STR_PATH)
        int_num = 1
        for str_json in list_users:
            # 筛选JSON文件（.json）
            if str_json != 'admin.json' and re.compile('^(.*json)$').match(str_json) != None:
                self.dict_json_files[str(int_num)] = str_json.replace('.json', '')
                int_num += 1
            else:
                pass
        # 输入修改用户编号
        str_intput = self.input_operate('用户编号', self.dict_json_files)
        str_update_user = self.dict_json_files.get(str_intput)
        if str_update_user != None:
            str_user_file = '%s\\%s.json' % (STR_PATH, str_update_user)
            Manage.auth(str_user_file, str_update_user, self.dict_operate_type)
        else:
            print('用户%s不存在' % str_update_user)
            self.start_operate(self.dict_user_info)


def login():
    '【登录】'
    STR_LOG.debug('输入用户名、密码')
    str_username = input('请输入用户名：').strip()
    str_password = input('请输入密码：').strip()
    return check_login(str_username, str_password)


@Manage('check_user')
def check_login(str_username: str, str_password: str):
    '''【验证】
    str_username：用户名
    str_password：密码'''


def operate(dict_user_info: dict):
    '【操作】，dict_user_info：用户信息'
    if dict_user_info != None:
        STR_LOG.debug('用户%s登录成功，开始操作' % dict_user_info['username'])
        start(dict_user_info)


@Operate('start_operate')
def start(dict_user_info: dict):
    '【开始】，dict_user_info：用户信息'


def main():
    try:
        operate(login())
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
