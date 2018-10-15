import xlrd
import xlwt

def process_origin_excel(origin_xls,output_xls):
    workbook = xlrd.open_workbook(origin_xls)
    print(workbook.sheet_names()) # [u'sheet1', u'sheet2']
    sheet = workbook.sheet_by_index(0)

    # 写出excel
    write_workbook = xlwt.Workbook()
    write_sheet = write_workbook.add_sheet("sheet1",cell_overwrite_ok=True)
    print((sheet.cell(2,3)))
    print(sheet.nrows,sheet.ncols)
    merge_cell = (sheet.merged_cells)

    for row_num in range(sheet.nrows):
        for col_num in range(sheet.ncols):
            if(sheet.cell_value(row_num,col_num)!=""):
                temp_data = (sheet.cell_value(row_num,col_num))
                write_sheet.write(row_num, col_num, temp_data)

    for cell in merge_cell:
        if (cell[1] != cell[0]+1) :
            print(cell)
            merge_cell_fill(sheet,cell,write_sheet)
    write_workbook.save(output_xls)

def merge_cell_fill(read_sheet,merge_list,write_sheet):
    left_row = merge_list[0]
    right_row = merge_list[1]
    low_col = merge_list[2]
    high_col = merge_list[3]

    for row in range(left_row,right_row):
        for col in range(low_col,high_col):
            #sheet.cell_value(row,col) = sheet.cell(left_row,low_col)
            temp_data = read_sheet.cell_value(left_row,low_col)
            write_sheet.write(row,col,temp_data)


def  data_split_parse(data,length, parse_list)
    if len(parse_list) == 2:
        parse_start = parse_list[0]
        parse_end = parse_list[1]
    elif len(parse_list) == 1:
        parse_start = parse_end = parse_list[0]
    else:
        pass



if __name__ == "__main__":
    #处理原始的excel,输出一个填充了各个空格的excel
    process_origin_excel("dp_cc_reg.xlsx","dp_fill_1.xls")
    #按行处理新的excel,将每行的数据存入到字典中
