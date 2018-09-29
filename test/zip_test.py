# coding:utf-8
# zip_test.py
# yang.wenbo


import os
import zipfile

STR_PATH = os.path.dirname(os.path.abspath(__file__))


class Test_Zip:

    def __init__(self):
        pass

    def test_zip(self):
        os.chdir(('%s\\files' % STR_PATH))
        zip_obj = zipfile.ZipFile('test.zip', 'w')
        zip_obj.write('test.txt', compress_type=zipfile.ZIP_DEFLATED)
        zip_obj.close()

    def test_unzip(self):
        os.chdir(('%s\\files' % STR_PATH))
        zip_obj = zipfile.ZipFile('test.zip')
        zip_obj.extractall()


def main():
    zip_obj = Test_Zip()
    zip_obj.test_zip()
    zip_obj.test_unzip()

if __name__ == '__main__':
    main()
