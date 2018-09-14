# coding:utf-8
# http_server.py
# yang.wenbo


import socket


class HTTPServer:
    '服务类'

    def __init__(self, str_host: str, int_port: int, int_buffer_size: int):
        '''【初始化】
        str_host：访问设置：localhost（本机）、IP值（IP）、空（任意主机）
        int_port：端口
        tuple_addr：地址(str_host, int_port)
        int_bsize_size：缓存（B）'''
        self.str_host = str_host
        self.int_port = int_port
        self.tuple_addr = (str_host, int_port)
        self.int_buffer_size = int_buffer_size

    def start(self):
        '【开启】'
        # 新建socket
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP-SOCK_STREAM，UDP-SOCK_DGRAM
        # 绑定地址
        socket_obj.bind(self.tuple_addr)
        # 监听连接的数量
        socket_obj.listen(1)
        # 启动服务，循环发送、接收数据
        print('启动HTTP服务')
        while True:
            # 等待连接
            print('等待连接...')
            socket_conn_obj, tuple_conn_addr = socket_obj.accept()
            print('成功连接：', tuple_conn_addr)
            # 接收数据
            data_obj = socket_conn_obj.recv(self.int_buffer_size)
            # print('收到数据：', data_obj)
            if data_obj:
                # 收到数据第一行：GET / HTTP/1.1
                # 收到数据第一行：GET /json HTTP/1.1
                # 收到数据第一行：GET /pic/pig.jpg HTTP/1.1
                request_path = data_obj.decode('utf-8').splitlines()[0]
                str_method, str_path, str_http = request_path.split()
                print('切换URL地址到：', str_path)
                str_response = ''
                # 页面输出
                if str_path == '/':
                    str_response = self.show_homepage()
                elif str_path == '/json':
                    str_response = self.show_json({'method': str_method, 'path': str_path, 'http': str_http})
                elif str_path == '/pic/pig.jpg':
                    str_response = self.show_image()
                else:
                    str_response = self.show_error()
                socket_conn_obj.sendall(str(str_response).encode())
            else:
                pass

            socket_conn_obj.close()

    def show_homepage(self):
        return '''HTTP/1.1 200 OK

        <h1>Hello World</h1>'''

    def show_json(self, dict_json: dict):
        return (f'''HTTP/1.1 200 OK

        <h1>Hello World</h1>
        {dict_json}''')

    def show_image(self):
        return (f'''HTTP/1.1 200 OK

        <h1>Hello World</h1>
        <img src="https://t3.ftcdn.net/jpg/01/45/55/74/240_F_145557487_vHGwaSDnPxcTRDP4UdL3wGh0aWRpfhrQ.jpg" width="300" height="150">''')

    def show_error(self):
        return '''HTTP/1.1 200 OK

        <h1>404</h1>'''


def main():
    server_obj = HTTPServer('', 8888, 1024)
    server_obj.start()

if __name__ == '__main__':
    main()
