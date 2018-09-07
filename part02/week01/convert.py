# coding:utf-8
# convert.py
# yang.wenbo

# 1.欢迎使用转换器
print('欢迎使用转换器'.center(30, '='))

# 2.设置转换类型
dict_convert_type = {
    'C': '摄氏度',
    'F': '华氏度',
    'M': '米',
    'T': '英尺',
    'P': '人民币',
    'U': '美元'
}

# 3.开启转换器
while True:

    # 3.1.输入转换类型
    str_input_type = input('请输入首字母，选择转换类型：\n' + 'C.摄氏度转华氏度\n' + 'F.华氏度转摄氏度\n' + 'M.米转英尺\n' + 'T.英尺转米\n' + 'P.人民币转美元\n' + 'U.美元转人民币\n').upper()

    # 3.2.判断输入内容是否为正确的转换类型
    bool_input = False
    while bool_input == False:
        if dict_convert_type.get(str_input_type) == None:
            str_input_type = input('请重新输入正确的首字母，选择转换类型：\n' + 'C.摄氏度转华氏度\n' + 'F.华氏度转摄氏度\n' + 'M.米转英尺\n' + 'T.英尺转米\n' + 'P.人民币转美元\n' + 'U.美元转人民币\n').upper()
        else:
            bool_input = True

    # 3.3.输入转换的值
    str_input_value = input('请输入转换的值')

    # 3.4.判断输入内容是否为数字
    bool_input = False
    while bool_input == False:
        if str_input_value.replace('.', '').isdigit() == False:
            str_input_value = input('转换的值必须是数字，请重新输入：')
        else:
            bool_input = True

    # 3.5.转换
    str_output_type = ''
    str_output_value = 0.0
    if str_input_type == 'C':
        str_output_type = 'F'
        str_output_value = float(str_input_value)*9/5+32
    elif str_input_type == 'F':
        str_output_type = 'C'
        str_output_value = (float(str_input_value)-32)*5/9
    elif str_input_type == 'M':
        str_output_type = 'T'
        str_output_value = float(str_input_value)*3.2808
    elif str_input_type == 'T':
        str_output_type = 'M'
        str_output_value = float(str_input_value)*0.3048
    elif str_input_type == 'P':
        str_output_type = 'U'
        str_output_value = float(str_input_value)*0.1461
    elif str_input_type == 'U':
        str_output_type = 'P'
        str_output_value = float(str_input_value)*6.8458
    else:
        pass

    # 3.6.输出
    print('%s%s等于%f%s' % (str_input_value, dict_convert_type[str_input_type], round(str_output_value, 4), dict_convert_type[str_output_type]))

    # 3.7.按q键退出转换器，按其他任意键继续
    str_control = input("按q键退出，按其他任意键继续：").lower()
    if str_control == 'q':
        break
    else:
        pass
