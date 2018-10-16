with open("test_asic_reg.bin","wb") as f:
    for i in range(5000):
        f.write((i-500).to_bytes(4,byteorder="little",signed = True))

