import openpyxl as openpyxl

DEFAULT_SHEET_ONE = 'Sheet1'


# 获取excel的表
def get_sheet(excel_file, sheet_name):
    wb = openpyxl.load_workbook(excel_file)
    return wb.get_sheet_by_name(sheet_name)
