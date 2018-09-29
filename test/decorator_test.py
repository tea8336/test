# coding:utf-8
# decorator_test.py
# yang.wenbo


# def aaa(aaa):
#     def bbb():
#         print('bbb')
#         return aaa()
#     print('aaa')
#     return bbb

# @aaa
# def ccc():
#     print('ccc')

# for int_i in range(3):
#     print('===')
#     ccc()


# print('@：aaa')
# def ccc():
#     def bbb():
#         print('bbb')
#     bbb()
#     print('ccc')

# for int_i in range(3):
#     print('===')
#     ccc()


# import os
# from functools import wraps

# def aaa(aaa):
#     # @wraps(aaa)
#     def bbb(*ddd):
#         print(ddd[0])
#         print('bbb')
#         return aaa(*ddd)
#     print('aaa')
#     return bbb

# @aaa
# def ccc(ddd):
#     print(f'*{ccc.__name__}*')

# for int_i in range(2):
#     print('===')
#     ccc('ddd')
