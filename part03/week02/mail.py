# coding:utf-8
# mail.py
# yang.wenbo


import smtplib

from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class Mail:
    '邮件类'

    def __init__(self, str_from_addr: str, str_password: str, str_smtp_server='smtp.qq.com'):
        '【初始化】'
        self.smtp_obj = SMTP_SSL(str_smtp_server)
        # smtp_obj.set_debuglevel(1)
        self.smtp_obj.ehlo(str_smtp_server)
        self.smtp_obj.login(str_from_addr, str_password)
        self.str_from_addr = str_from_addr

    def mail_send(self, str_title: str, str_body: str, list_to_addrs: list, str_mailtype: str = 'plain', file_attachment: str = None):
        '''【发送邮件】
        str_title: 邮件标题
        str_body: 邮件内容
        list_to_addrs：接收地址
        str_mailtype 邮件类型，默认是文本，发html时候指定为html
        file_attachment 附件'''
        # 构造一个MIMEMultipart对象代表邮件本身
        mail_obj = MIMEMultipart()
        mail_obj["Subject"] = Header(str_title, "utf-8")
        mail_obj["from"] = self.str_from_addr
        # TODO 发送邮件
        try:
            # 发送地址
            mail_obj['To'] = ','.join(list_to_addrs)
            # mailtype代表邮件类型，纯文本或html等
            mail_obj.attach(MIMEText(str_body, str_mailtype, 'utf-8'))  
            # 有附件内容，才添加到邮件
            if file_attachment:
                # 二进制方式模式文件
                with open(file_attachment, 'rb') as file_obj:
                    # MIMEBase表示附件的对象
                    mime_obj = MIMEBase('text', 'txt', filename=file_attachment)  
                    # filename是显示附件名字
                    mime_obj.add_header('Content-Disposition', 'file_attachment', filename=file_attachment)  
                    # 获取附件内容
                    mime_obj.set_payload(file_obj.read())
                    encoders.encode_base64(mime_obj)
                    # 作为附件添加到邮件
                    mail_obj.attach(mime_obj)  
            self.smtp_obj.sendmail(self.str_from_addr, list_to_addrs, mail_obj.as_string())
            self.smtp_obj.quit()
            print('发送成功')
        except smtplib.SMTPException as e:
            print('发送失败')
            print(e)


def mail_from_addr() -> str:
    '【发送地址】'
    return '发件人邮箱'


def mail_password() -> str:
    '【密码】'
    return '密码'


def mail_to_addrs() -> list:
    '【接收地址】'
    return ['收件人邮箱']


def main():
    try:
        list_pdf = []
        for int_i in range(1, 6):
            list_pdf.append('第%i行' % int_i)

        mail_obj = Mail(mail_from_addr(), mail_password())
        mail_obj.mail_send('测试邮件', 'study.python', mail_to_addrs())
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
