class dp_cc_regs_class():
    # 可以动态的添加类的成员，现在先静态实现。
    def __init__(self,offset,
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
                 description):
        self.offset = offset
        self.regname = regname
        self.short_des = short_description
        self.width = width
        self.bit = bit
        self.fieldname = fieldname
        self.description = description




