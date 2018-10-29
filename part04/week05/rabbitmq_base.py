# coding:utf-8
# rabbitmq_base.py
# yang.wenbo


import sys
import pika

from log import Log


DICT_CONFIG = {
    "username": "ywb",
    "password": "admin",
    "host": "192.168.247.130",
    "port": "15672"
}


class Rabbitmq_Base:
    def __init__(self):
        '【初始化】'
        Log().log_print().info('init Rabbitmq_Base...')
        self.obj_connection = self.make_connect()
        self.obj_channel = self.obj_connection.channel()

    def make_connect(self):
        '【连接】'
        Log().log_print().info('make_connect...')
        obj_creds = pika.PlainCredentials(DICT_CONFIG["username"], DICT_CONFIG["password"])
        obj_params = pika.ConnectionParameters(DICT_CONFIG["host"], credentials=obj_creds)
        return pika.BlockingConnection(obj_params)

    def make_queue(self, str_queue_name):
        '【队列】'
        Log().log_print().info('make_queue...')
        self.obj_channel.queue_declare(queue=str_queue_name, durable=True)

    def make_random_queue(self):
        '【随机队列】'
        Log().log_print().info('make_random_queue...')
        return self.obj_channel.queue_declare(exclusive=True).method.queue

    def consume(self, callback, str_queue_name, bool_noack=False):
        '【消费】'
        Log().log_print().info('consume...')
        self.obj_channel.basic_qos(prefetch_count=1)
        self.obj_channel.basic_consume(callback, queue=str_queue_name, no_ack=bool_noack)
        self.obj_channel.start_consuming()

    def close_connect(self):
        '【关闭】'
        Log().log_print().info('close_connect...')
        self.obj_connection.close()
