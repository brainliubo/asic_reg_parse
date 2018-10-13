import xlrd

def read_excel():
    workbook = xlrd.open_workbook(r'dp_cc_reg1.xls',formatting_info=True)
    print(workbook.sheet_names()) # [u'sheet1', u'sheet2']
    sheet = workbook.sheet_by_index(0)
    print((sheet.cell(2,3)))
    print(sheet.nrows,sheet.ncols)


if __name__ == "__main__":
    read_excel()