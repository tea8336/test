# coding:utf-8
# pdf.py
# yang.wenbo


import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('simsun', 'C:\\WINDOWS\\Fonts\\simsun.ttc'))


class PDF:
    'PDF类'

    def __init__(self, list_pdf: list, str_name: str, bool_is_custom_color: bool = False, tulpe_color: tuple = (0.77, 0.77, 0.77), int_font_size: int = 18, float_offset_x: float = 5, float_offset_y: float = 5):
        '''【初始化】
        list_pdf：保存的内容
        str_name：保存的文件名'''
        self.str_path = os.path.dirname(os.path.abspath(__file__))
        self.list_pdf = list_pdf
        self.str_name = '%s\\files\\%s.pdf' % (self.str_path, str_name)
        self.bool_is_custom_color = bool_is_custom_color
        self.int_font_size = int_font_size
        self.float_offset_x = float_offset_x
        self.float_offset_y = float_offset_y

    def save_pdf(self):
        '【保存PDF】'
        canvas_pdf = canvas.Canvas(self.str_name, pagesize=A4)
        # 纸张大小
        float_width, float_height = A4

        # # 颜色
        # if self.is_custom_color:
        #     canvas_pdf.setFillColorRGB(color)

        # 字体
        canvas_pdf.setFont("simsun", self.int_font_size)

        # PDF
        canvas_obj = canvas_pdf.beginText()

        # 起始位置
        canvas_obj.setTextOrigin(10, float_height - self.float_offset_y * 10)

        # 写入
        for data_pdf in self.list_pdf:
            canvas_obj.textLine(data_pdf)

        canvas_pdf.drawText(canvas_obj)
        canvas_pdf.showPage()
        canvas_pdf.save()
        print('保持成功')


def main():
    list_pdf = []
    for int_i in range(1, 6):
        list_pdf.append('第%i行' % int_i)

    pdf_obj = PDF(list_pdf, 'study')
    pdf_obj.save_pdf()

if __name__ == '__main__':
    main()
