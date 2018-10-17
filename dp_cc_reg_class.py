class dp_cc_regs_class():
    # 可以动态的添加类的成员，现在先静态实现。
    def __init__(self,
                 excel_row_index,
                 offset,
                 regname,
                 short_description,
                 width,
                 other,
                 pr,
                 bit,
                 fieldname,
                 rw,
                 reset_value,
                 set_or_clear,
                 misc,
                 description,
                 field_value = None):
        self.excel_row_index = excel_row_index
        self.offset = offset
        self.regname = regname
        self.short_des = short_description
        self.width = width
        self.bit = bit
        self.fieldname = fieldname
        self.rw = rw
        self.reset_value = reset_value
        self.set_or_clear = set_or_clear
        self.misc = misc
        self.description = description
        self.parse_field_value = field_value




