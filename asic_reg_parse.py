import xlrd
import xlwt
from dp_cc_reg_class import dp_cc_regs_class
import struct
import  os

'''
process_origin_excel: 处理原始的excel,主要是merge_cell,将Merge_cell的值填充到各个cell,输出到新的excel中
'''
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

'''
merge_cell_fill: 处理excel中合并的表格，将合并中的各个表格值填充，形成新的表格
'''
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

'''
process_filled_excel:对填充后的新表格进行按行读取，将信息填充到 class list
'''
def process_filled_excel(filled_excel):
    workbook = xlrd.open_workbook(filled_excel)
    sheet = workbook.sheet_by_index(0)
    reg_content_list = []
    for row_num in range(sheet.nrows):
        row_content = sheet.row_values(row_num,0,sheet.ncols)
        temp_reg_class = dp_cc_regs_class((row_content[0]),
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

    return reg_content_list

'''
read_datafile: 读取二进制的文件，根据输入端模式进行大小端模式读取，并根据单个data的长度进行解码
               将数据地址和长度以dict的方式进行存储。
'''
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
            key_value = "0x"+ hex(data_address).replace("0x","").zfill(4) #0x4-->0x0004,保证key值和reg中的值一致
            address_data_dict[key_value] = unpack_data

    return  address_data_dict

'''
reg_field_parse: 根据reg_filed,以及data,进行位段的解析，结果存储在list中
'''
def reg_field_parse(reg_class,data):
    bit = reg_class.bit
    bit = bit.lstrip("[")
    bit_list = bit.rstrip("]").split(":")
    print(type(bit_list))
    print(bit_list)
    if (len(bit_list) == 1):
        start_field = end_field = bit_list[0]
    else :
        end_field = bit_list[0]
        start_field = bit_list[1]
    print(start_field, end_field)

    #解析位段

    pass


'''
reg_parse: 根据reg_filed,以及data,进行所有的reg
'''
def reg_parse(reg_content_row_list,data_dict):
    for row_class in reg_filed_content_list:
        if  data_dict.get(row_class.offset) is not None:  # exclued the row_list which is not regs
            #print(row_class.offset)
            #print(type(data_dict.get(row_class.offset)))
            (data,) = data_dict.get(row_class.offset)  # 获取该地址对应的数据
            #print(data)
            #解析数据filed:
            reg_field_parse(row_class,data)



if __name__ == "__main__":
    reg_filed_content_list = []
    data_file_dict = {}

    #处理原始的excel,输出一个填充了各个空格的excel
    process_origin_excel("dp_cc_reg.xlsx","dp_fill_1.xls")

    #按行处理新的excel,将每行的数据存入到列表中，每个元素都是class
    reg_filed_content_list = process_filled_excel("dp_fill_1.xls")

    #读取数据,按照大小端进行处理和解析
    data_file_dict = read_datafile("test_asic_reg.bin",0,4)

    # 解析数据
    reg_parse(reg_filed_content_list,data_file_dict)
    #输出到excel中

    pass
