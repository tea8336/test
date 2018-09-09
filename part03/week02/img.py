# coding:utf-8
# img.py
# yang.wenbo


import os
import re
import openpyxl

from PIL import Image


class Imge:
    '图片类'

    def __init__(self):
        '【初始化】'
        self.str_path = os.path.dirname(os.path.abspath(__file__))
        self.dict_image_file = {}
        self.dict_image_ID = {}

    def image_info(self, str_path: str):
        '【打印图片信息】，str_path：图片目录'
        # 读取文件
        list_files = os.listdir(str_path)
        # 筛选图片文件（.jpg|.png|.bmp）
        int_num = 1
        for str_file_name in list_files:
            if self.check_file(str_file_name):
                int_size = os.path.getsize(os.path.join(str_path, str_file_name))//1024
                str_size = ('%iKB' % int_size)
                self.dict_image_file[str_file_name] = str_size
                self.dict_image_ID[int_num] = str_file_name
                int_num += 1
            else:
                continue

        if len(self.dict_image_file) > 0:
            for str_k in sorted(self.dict_image_ID.keys()):
                print('%s.%s:%s' % (str_k, self.dict_image_ID[str_k], self.dict_image_file[self.dict_image_ID[str_k]]))
        else:
            print('%s文件夹中没有图片文件（.jpg|.png|.bmp）' % str_name)
        pass

    def check_file(self, str_file: str) -> bool:
        '【校验图片文件.jpg|.png|.bmp】，校验结果：正确返回True，错误返回False'
        re_file = re.compile('^(.*jpg|.*png|.*bmp)$')
        if re_file.match(str_file) == None:
            return False
        else:
            return True

    def image_rotate(self, str_path: str):
        '''【图片·旋转】
        str_path：图片目录
        int_rotate：旋转的角度'''
        # 操作的图片
        str_image = input('请输入操作的图片：')
        # 图片是否存在
        str_image_path = os.path.join(str_path, str_image)
        if os.path.exists(str_image_path) == False:
            print('图片文件不存在')
            return
        # TODO 旋转图片
        try:
            int_rotate = int(input('请输入旋转角度（如：90）：'))
            image_obj = Image.open(str_image_path)
            image_obj.rotate(int_rotate).save(str_image_path)
            self.image_show(str_image_path)
            print('旋转成功')
        except Exception as e:
            print('输入角度错误，旋转失败')

    def image_show(self, str_image_path: str):
        '【显示图片】，str_image_path：图片目录'
        image_obj = Image.open(str_image_path)
        image_obj.show()


def main():
    try:
        str_path = ('%s\\files' % os.path.dirname(os.path.abspath(__file__)))
        image_obj = Imge()
        image_obj.image_info(str_path)
        image_obj.image_rotate(str_path)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
