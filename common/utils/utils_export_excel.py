# coding=UTF-8
'''
Created on 2015年7月7日

@author: tianxiaohe
'''
import math
import StringIO

from django.http.response import HttpResponse

import xlwt
from common.utils.utils_log import log


"""
导出excel
export_excel(title,columns=[],data_list=[])
title:标题
columns：列头字段
data_list：数据
"""
def export_excel(title='',columns=[],data_list=[]):
    """导出excel"""
    response = HttpResponse(content_type = "application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % title
    
    """设置单元格边框为1"""
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.bottom_colour=0x3A

    badBG = xlwt.Pattern()
    badBG.pattern = 2
    badBG.pattern_fore_colour = 3

    """数据填充单元格的样式"""
    style_column = xlwt.easyxf("align: wrap on, vert centre, horiz left;")
    style_column.borders = borders

    """列头单元格的样式"""
    style_head = xlwt.XFStyle()
    style_head.borders = borders
    style_head.pattern = badBG

    """标题的样式"""
    style_heading = xlwt.easyxf("pattern: pattern solid, fore_color white; font: height 300, name Arial, colour_index black, bold off; align: wrap on, vert centre, horiz center;")
    style_heading.borders = borders
    wb = xlwt.Workbook(encoding = 'utf-8')
    
    column_count = len(data_list)

    if column_count:
        """xls最多只允许有65536行，为避免出错，再此默认设置为50000行一页"""
        try:
            sheet_count = int(math.ceil(column_count/50000.0))
            for i in range(0,sheet_count):

                sheet = wb.add_sheet(title+"sheet"+str(i))
                """设置列头及每列宽度，宽度默认为1"""
                for j, column in enumerate(columns):
                    sheet.write(0,j,column['name'],style_head)
                    column_width = 1;
                    if column.has_key('width'):
                        column_width = column['width']
                    sheet.col(j).width = 0x0d00*column_width

                """开始填充数据"""
                row = 1
                end_row = (i+1)*50000
                if end_row>=column_count:
                    end_row = column_count
                for m in range(i*50000,end_row ):
                    for n, column in enumerate(columns):
                        sheet.write(row,n,data_list[m][column['key']],style_column)
                    row=row + 1
            output = StringIO.StringIO()
            wb.save(output)
            output.seek(0)
            response.write(output.getvalue())
        except Exception,e:
            log.error('create export_default error, e=%s' % (e))
    else:
        sheet = wb.add_sheet(title)
        sheet.write_merge(0, 1, 0,6, '没有满足条件的数据！',style_heading)
        output = StringIO.StringIO()
        wb.save(output)
        output.seek(0)
        response.write(output.getvalue())
    return response
