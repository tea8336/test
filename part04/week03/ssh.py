# coding:utf-8
# ssh.py
# yang.wenbo


import os
import sys
import string
import argparse
import paramiko
import configparser

STR_PATH = '%s\\files' % os.path.dirname(os.path.abspath(__file__))
STR_CONFIG = 'config.ini'

from log import Log


class AcceptPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return


class SSH:

    def __init__(self):
        '【初始化】'
        Log().log_print().info('init SSH...')
        self.client_obj = object

    def ssh_connect(self, str_host, str_user, str_pwd):
        '【连接服务器】'
        Log().log_print().info('ssh_connect...')
        try:
            self.client_obj = paramiko.SSHClient()
            self.client_obj.set_missing_host_key_policy(AcceptPolicy())
            self.client_obj.connect(str_host, username=str_user, password=str_pwd)
            return self.client_obj, True
        except Exception as e:
            return self.client_obj, False

    def ssh_command(self, str_cmd):
        '【command发送命令】'
        Log().log_print().info('ssh_command...')
        try:
            standard_input, standard_out, standard_error = self.client_obj.exec_command(str_cmd)
            print(standard_out.read().decode())
            print(standard_error.read().decode())
            return standard_out
        except Exception as e:
            print(e)

    def ssh_upload(self, str_local_file, str_remote_file):
        '【上传文件】'
        Log().log_print().info('ssh_upload...')
        dict_result = {'status': 0, 'msg': 'ok'}
        try:
            if os.path.exists(str_local_file) == False:
                dict_result['status'] = 3
                dict_result['msg'] = '文件{}不存在'.format(str_local_file)
                return
            if self.client_obj:
                ftp_client_obj = self.client_obj.open_sftp()
                ftp_client_obj.put(str_local_file, str_remote_file)
                ftp_client_obj.close()
            else:
                dict_result['status'] = 1
                dict_result['msg'] = 'error'
        except paramiko.SSHException as e:
            print(e)
            dict_result['status'] = 2
            dict_result['msg'] = e
        finally:
            return dict_result

    def ssh_download(self, str_local_file, str_remote_file):
        '【下载文件】'
        Log().log_print().info('ssh_download...')
        dict_result = {'status': 0, 'msg': 'ok'}
        try:
            if self.client_obj:
                ftp_client_obj = self.client_obj.open_sftp()
                ftp_client_obj.get(str_remote_file, str_local_file)
                ftp_client_obj.close()
            else:
                dict_result['status'] = 1
                dict_result['msg'] = 'error'
        except paramiko.SSHException as e:
            Log().log_print().warning(e)
            dict_result['status'] = 2
            dict_result['msg'] = e
        finally:
            return dict_result

    def ssh_colse(self):
        '【关闭连接】'
        Log().log_print().info('ssh_close...')
        self.client_obj.close()


class Cfg:

    def __init__(self):
        '【初始化】'
        Log().log_print().info('init Cfg...')

    @staticmethod
    def write_config(str_host, str_user, str_pwd):
        '【写入配置文件】'
        Log().log_print().info('write_config...')
        try:
            config_file = configparser.ConfigParser()
            config_file.read(STR_CONFIG)
            config_file[str_host] = {}
            config_file[str_host]['user'] = str_user
            config_file[str_host]['pwd'] = str_pwd
            with open(STR_CONFIG, 'w') as file_obj:
                    config_file.write(file_obj)
            Log().log_print().info('添加主机IP：{}成功'.format(str_host))
        except Exception as e:
            Log().log_print().info('添加主机IP：{}失败'.format(str_host))

    @staticmethod
    def load_config(str_host):
        '【读取配置文件】'
        Log().log_print().info('load_config...')
        config_file = configparser.ConfigParser()
        config_file.read(STR_CONFIG)
        if str_host == 'all':
            return config_file.sections()
        elif str_host == 'operate':
            return config_file[str_host]
        else:
            return config_file[str_host]['user'], config_file[str_host]['pwd']


def feature_list():
    '【功能列表】'
    Log().log_print().info('feature_list...')
    parser_obj = argparse.ArgumentParser('ywb SSH 【功能列表】')
    group_config = parser_obj.add_argument_group('配置命令')
    group_config.add_argument('-a', '--addhost', metavar='hostinfo', nargs=3, dest='addhost', action='store', help='添加主机IP：第一个参数主机IP，第二个参数用户名，第三个参数密码')
    group_base = parser_obj.add_argument_group('基本命令')
    group_base.add_argument('-s', '--server', metavar='ipaddrs', nargs='+', dest='server', action='store', help='连接服务器：可连接多个IP地址')
    group_base.add_argument('-c', '--control', dest='control', action='store_true', help='控制台命令')
    group_base.add_argument('-e', '--exit', dest='exit', action='store_true', help='退出服务器')
    group_operate = parser_obj.add_argument_group('功能命令')
    group_operate.add_argument('-u', '--upload', metavar='files', nargs=2, dest='upload', action='store', help='上传文件：第一个参数本地文件，第二个参数远程文件')
    group_operate.add_argument('-d', '--download', metavar='files', nargs=2, dest='download', action='store', help='下载文件：第一个参数本地文件，第二个参数远程文件')
    return parser_obj, parser_obj.parse_args()


def check_hosts(list_hosts):
    '【验证主机IP是否在配置文件中】'
    Log().log_print().info('check_hosts...')
    config_file = configparser.ConfigParser()
    config_file.read(STR_CONFIG)
    for str_host in list_hosts:
        if config_file.sections().count(str_host) < 1:
            print('IP地址：{}不存在，请先添加主机IP'.format(str_host).center(30, '='))
            return False
    return True


def start_params(parser_obj, input_args):
    '【有参数开始运行】'
    Log().log_print().info('start_params...')
    dict_hosts = {}
    if input_args.addhost:
        Cfg().write_config(input_args.addhost[0], input_args.addhost[1], input_args.addhost[2])
    if input_args.server:
        if check_hosts(input_args.server):
            for str_host in input_args.server:
                ssh_obj = SSH()
                print('正在连接IP：{}...'.format(str_host))
                client_obj, bool_result = start_connection(ssh_obj, str_host)
                if bool_result:
                    print('IP：{}连接成功'.format(str_host).center(30, '='))
                    dict_hosts[str_host] = ssh_obj
                else:
                    print('IP：{}连接失败'.format(str_host).center(30, '='))
                    dict_hosts.clear()
                    return
    else:
        print('请连接服务器')
    return dict_hosts


def start_noparams(list_host):
    '【无参数开始运行】'
    Log().log_print().info('start_noparams...')
    dict_hosts = {}
    if check_hosts(list_host):
        for str_host in list_host:
            ssh_obj = SSH()
            print('正在连接IP：{}...'.format(str_host))
            client_obj, bool_result = start_connection(ssh_obj, str_host)
            if bool_result:
                print('IP：{}连接成功'.format(str_host).center(30, '='))
                dict_hosts[str_host] = ssh_obj
            else:
                print('IP：{}连接失败'.format(str_host).center(30, '='))
                dict_hosts.clear()
    return dict_hosts


def start_connection(ssh_obj, str_host):
    '【运行连接】'
    Log().log_print().info('start_connection...')
    str_user, str_pwd = Cfg().load_config(str_host)
    client_obj, bool_result = ssh_obj.ssh_connect(str_host, str_user, str_pwd)
    return client_obj, bool_result


def choose_host(list_hosts):
    '【选择操作的主机IP】'
    Log().log_print().info('choose_host...')
    if len(list_hosts) == 1:
        return list_hosts[0]
    else:
        for int_index in range(len(list_hosts)):
            print('{}.{}'.format(str(int_index), list_hosts[int_index]))
        str_input = input('请选择要操作的主机IP编号：')
        if int(str_input) < len(list_hosts):
            return list_hosts[int(str_input)]
        else:
            print('输入的编号不在列表中！')
            return choose_host(list_hosts)


def operate_control(ssh_obj):
    '【无参数编译，操作选择】'
    Log().log_print().info('operate_control...')
    while True:
        section_ctls = Cfg().load_config('operate')
        for section_ctl in section_ctls:
            print('{}.{}'.format(section_ctl, section_ctls[section_ctl]))
        str_cmd = input('>>>').lower()
        if str_cmd == 'u':
            str_local_file = input('请输入本地文件地址：')
            str_remote_file = input('请输入远程文件地址：')
            list_local_files = str_local_file.split(',')
            list_remote_files = str_remote_file.split(',')
            if len(list_local_files) != len(list_remote_files):
                print('文件数量不匹配！')
            else:
                for int_index in range(len(list_local_files)):
                    result_json = ssh_obj.ssh_upload(list_local_files[int_index], list_remote_files[int_index])
                    print(result_json)
        elif str_cmd == 'd':
            str_local_file = input('请输入本地文件地址：')
            str_remote_file = input('请输入远程文件地址：')
            list_local_files = str_local_file.split(',')
            list_remote_files = str_remote_file.split(',')
            if len(list_local_files) != len(list_remote_files):
                print('文件数量不匹配！')
            else:
                for int_index in range(len(list_local_files)):
                    result_json = ssh_obj.ssh_download(list_local_files[int_index], list_remote_files[int_index])
                    print(result_json)
        elif str_cmd == 'e':
            while True:
                str_cmd_ctl = input('#（【q】退出）')
                if str_cmd_ctl == 'q':
                    return
                else:
                    ssh_obj.ssh_command(str_cmd_ctl)
        elif str_cmd == 'q':
            ssh_obj.ssh_colse()
            break
        else:
            print('没有这个命令')


def operate_params():
    '【有参数编译】'
    Log().log_print().info('operate_params...')
    parser_obj, input_args = feature_list()
    dict_hosts = start_params(parser_obj, input_args)           
    if dict_hosts != None and len(dict_hosts) > 0:
        for str_host, ssh_obj in dict_hosts.items():
            print('{}'.format(str_host).center(30, '-'))
            if input_args.control:
                operate_control(ssh_obj)
            if input_args.exit:
                ssh_obj.ssh_colse()
            if input_args.upload:
                list_local_files = input_args.upload[0].split(',')
                list_remote_files = input_args.upload[1].split(',')
                if len(list_local_files) != len(list_remote_files):
                    print('文件数量不匹配！')
                else:
                    for int_index in range(len(list_local_files)):
                        result_json = ssh_obj.ssh_upload(list_local_files[int_index], list_remote_files[int_index])
                        print(result_json)
                # result_json = ssh_obj.ssh_upload(input_args.upload[0], input_args.upload[1])
                # print(result_json)
            if input_args.download:
                list_local_files = input_args.download[0].split(',')
                list_remote_files = input_args.download[1].split(',')
                if len(list_local_files) != len(list_remote_files):
                    print('文件数量不匹配！')
                else:
                    for int_index in range(len(list_local_files)):
                        if len(dict_hosts) > 1:
                            result_json = ssh_obj.ssh_download(str_host + list_local_files[int_index], list_remote_files[int_index])
                        else:
                            result_json = ssh_obj.ssh_download(list_local_files[int_index], list_remote_files[int_index])
                        print(result_json)
                # if len(dict_hosts) > 1:
                    # result_json = ssh_obj.ssh_download(str_host + input_args.download[0], input_args.download[1])
                # else:
                    # result_json = ssh_obj.ssh_download(input_args.download[0], input_args.download[1])
                # print(result_json)


def operate_noparams():
    '【无参数编译】'
    Log().log_print().info('operate_noparams...')
    print(''.center(30, '='))
    section_hosts = Cfg().load_config('all')
    for str_section_host in section_hosts:
        if str_section_host == 'operate' or str_section_host == 'path':
            continue
        print(str_section_host)
    print('a.添加主机IP')
    print('h.帮助')
    print('q.退出')
    str_input = input('请输入连接的主机IP（如：192.168.247.130）：')
    if str_input == 'a':
        str_host = input('请输入主机IP：')
        str_user = input('请输入用户名：')
        str_pwd = input('请输入密码：')
        Cfg().write_config(str_host, str_user, str_pwd)
        operate_noparams()
    elif str_input == 'h':
        parser_obj, input_args = feature_list()
        parser_obj.print_help()
        operate_noparams()
    elif str_input == 'q':
        return
    else:
        list_hosts = [str_host for str_host in str_input.split(' ') if str_host.strip() != '']
        dict_hosts = start_noparams(list_hosts)
        if dict_hosts != None and len(dict_hosts) > 0:
            for str_host, ssh_obj in dict_hosts.items():
                print('{}'.format(str_host).center(30, '-'))
                operate_control(ssh_obj)
        else:
            operate_noparams()


def main():
    try:
        print('欢迎使用'.center(30, '*'))
        os.chdir(STR_PATH)
        paramiko.util.log_to_file("study_paramiko.log")
        if len(sys.argv) == 1:
            operate_noparams()
        else:
            operate_params()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
