import xlrd
import xlwt
from dp_cc_reg_class import dp_cc_regs_class
import struct
import  os

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

def process_filled_excel(filled_excel):
    workbook = xlrd.open_workbook(filled_excel)
    sheet = workbook.sheet_by_index(0)
    reg_content_list = []
    for row_num in range(sheet.nrows):
        row_content = sheet.row_values(row_num,0,sheet.ncols)
        try:
            if ((row_content[0])):
                temp_reg_class = dp_cc_regs_class(int(row_content[0]),
                                                  row_content[1],
                                                  row_content[2],
                                                  row_content[3],
                                                  row_content[4],
                                                  row_content[5],
                                                  row_content[6],
                                                  row_content[7],
                                                  row_content[8],
                                                  row_content[9],
                                                  row_content[10],
                                                  row_content[11],
                                                  row_content[12])
                reg_content_list.append(temp_reg_class)
        except:
            pass
    return reg_content_list


def read_datafile(data_path,data_endding,single_data_size):
    address_data_dict = {}  # 空dict,按照地址和数据组成dict返回
    read_count = 0
    file_size_byte = (os.path.getsize(data_path))
    read_num = file_size_byte // single_data_size
    unpack_size = single_data_size//4
    unpack_pattern = str(unpack_size)+"i"
    print(unpack_pattern)
    print("file size = {},single_data_size = {},read_num = {}".format(file_size_byte,single_data_size,read_num))
    with open(data_path,"rb") as f:
        for read_count  in range(read_num):
            temp_data = f.read(single_data_size)
            unpack_data = struct.unpack(unpack_pattern,temp_data) # return tuple
            data_address = read_count * single_data_size
            address_data_dict[str(hex(data_address))] = unpack_data

    return  address_data_dict

        # while True:
        #     temp_data = (f.read())
        #     if (data_endding == 1):
        # unpack_data = (struct.unpack(">i",temp_data))  #大端模式使用
        # else:
        #     unpack_data = (struct.unpack("i",temp_data)) # 默认小端模式解包,
        # print(unpack_data)

if __name__ == "__main__":
    reg_filed_content_list = []
    data_file_dict = {}
    #处理原始的excel,输出一个填充了各个空格的excel
    process_origin_excel("dp_cc_reg.xlsx","dp_fill_1.xls")
    #按行处理新的excel,将每行的数据存入到列表中，每个元素都是class
    reg_filed_content_list = process_filled_excel("dp_fill_1.xls")

    #读取数据,按照大小端进行处理和解析
    data_file_dict = read_datafile("test_asic_reg.bin",0,4)

    # for item in data_file_dict.items():
    #     print(item)
    #
    #print(data_file_dict[reg_filed_content_list[1].offset])
    #输出到excel中

    pass
