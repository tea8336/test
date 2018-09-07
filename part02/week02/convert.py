# coding:utf-8
# convert.py
# yang.wenbo


class Temperature:
    '温度：提供摄氏度与华氏度互相转换的方法'

    @staticmethod
    def convert_c_to_f(float_c: float) -> float:
        '''【摄氏度转华氏度】
        float_c：摄氏度
        返回：华氏度'''
        return float_c * 9 / 5 + 32

    @staticmethod
    def convert_f_to_c(float_f: float) -> float:
        '''【华氏度转摄氏度】
        float_f：华氏度
        返回：摄氏度'''
        return (float_f-32) * 5 / 9


class Length:
    '长度：提供米和英尺互相转换的方法'

    @staticmethod
    def convert_m_to_t(float_m: float) -> float:
        '''【米转英尺】
        float_m：米
        返回：英尺'''
        return float_m * 3.2808

    @staticmethod
    def convert_t_to_m(float_t: float) -> float:
        '''【英尺转米】
        float_t：英尺
        返回：米'''
        return float_t * 0.3048


class Currency:
    '货币：提供人民币和美元互相转换的方法'

    @staticmethod
    def convert_u_to_y(float_u: float) -> float:
        '''【美元转人民币】
        float_u：美元
        返回：人民币'''
        return float_u * 6.8458

    @staticmethod
    def convert_y_to_u(float_y: float) -> float:
        '''【人民币转美元】
        float_y：人民币
        返回：美元'''
        return float_y * 0.1461


class Transfer:
    '主体程序'

    def __init__(self, dict_convert_type):
        '【设置转换类型】，dict_convert_type：转换类型'
        self.dict_convert_type = dict_convert_type

    def welcome(self):
        '【欢迎词】'
        print('欢迎使用转换器'.center(30, '='))

    def input_info(self, str_info: str, int_type: int) -> str:
        '''【输入提示】
        str_info：提示信息
        int_type：输入操作（0.输入转换类型  1.输入转换的值/完成转换后是否继续转换）'''
        if int_type == 0:
            print('%s，选择转换类型：' % str_info)
            for str_k in sorted(self.dict_convert_type.keys()):
                print(str_k, self.dict_convert_type[str_k])
            return input().upper()
        elif int_type == 1:
            return input('%s：' % str_info)
        else:
            pass

    def check_input(self, str_input: str, int_type: int) -> bool:
        '''【校验输入内容】
        str_input：输入内容
        int_type：校验类型（0.校验转换类型  1.校验转换的值）
        校验结果：正确返回True，错误返回False'''
        if int_type == 0:
            if self.dict_convert_type.get(str_input) == None:
                return False
            else:
                return True
        elif int_type == 1:
            return str_input.replace('.', '').isdigit()
        else:
            pass

    def input_convert(self, int_type: int) -> str:
        '''【输入内容】
        int_type：输入类型（0.输入转换类型  1.输入转换的值）
        0.输入转换类型，必须是转换类型中已经定义的，字母不区分大小写
        1.输入转换的值，必须是数字'''
        if int_type == 0:
            # 输入转换类型
            str_input_type = self.input_info('请输入首字母', 0)
            # 判断输入内容是否为正确的转换类型
            while self.check_input(str_input_type, 0) == False:
                str_input_type = self.input_info('请重新输入正确的首字母', 0)
            return str_input_type
        elif int_type == 1:
            # 输入转换的值
            str_input_value = self.input_info('请输入转换的值', 1)
            # 判断输入内容是否为数字
            while self.check_input(str_input_value, 1) == False:
                str_input_value = self.input_info('转换的值必须是数字，请重新输入', 1)
            return str_input_value
        else:
            pass

    def output_type(self, str_type: str) -> str:
        '''【转换后的类型】
        str_type：转换前的类型
        返回：转换后的类型'''
        if str_type == 'C':
            return '华氏度'
        elif str_type == 'F':
            return '摄氏度'
        elif str_type == 'M':
            return '英尺'
        elif str_type == 'T':
            return '米'
        elif str_type == 'U':
            return '人民币'
        elif str_type == 'Y':
            return '美元'
        else:
            pass

    def output_value(self, str_type: str, str_value: str) -> float:
        '''【转换后的值（转换计算）】
        str_type：转换类型
        str_value：转换的值
        返回：计算结果'''
        if str_type == 'C':
            return Temperature.convert_c_to_f(float(str_value))
        elif str_type == 'F':
            return Temperature.convert_f_to_c(float(str_value))
        elif str_type == 'M':
            return Length.convert_m_to_t(float(str_value))
        elif str_type == 'T':
            return Length.convert_t_to_m(float(str_value))
        elif str_type == 'U':
            return Currency.convert_u_to_y(float(str_value))
        elif str_type == 'Y':
            return Currency.convert_y_to_u(float(str_value))
        else:
            pass

    def convert_output(self, str_input_type: str, str_input_value: str, str_output_type: str, str_output_value: str):
        '''【输出转换结果】
        str_input_type：转换前的类型
        str_input_value：转换前的值
        str_output_type：转换后的类型
        str_output_value：转换后的值'''
        print('%s%s等于%f%s' % (str_input_value, self.dict_convert_type[str_input_type], round(str_output_value, 4), str_output_type))


def main():
    '程序入口'
    try:
        # 1.实例化主体程序类
        dict_convert_type = {
            'C': '摄氏度',
            'F': '华氏度',
            'M': '米',
            'T': '英尺',
            'U': '美元',
            'Y': '人民币'
        }
        transfer = Transfer(dict_convert_type)
        # 2.欢迎使用转换器
        transfer.welcome()
        # 3.开启转换器
        while True:
            # 3.1.输入转换类型
            str_input_type = transfer.input_convert(0)
            # 3.2.输入转换的值
            str_input_value = transfer.input_convert(1)
            # 3.3.转换并输出结果
            transfer.convert_output(str_input_type, str_input_value, transfer.output_type(str_input_type), transfer.output_value(str_input_type, str_input_value))
            # 3.4.按q键退出转换器，按其他任意键继续
            if transfer.input_info('按q键退出，按其他任意键继续', 1).lower() == 'q':
                break
            else:
                pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
