# -*- coding: utf-8 -*- 
import xdrlib , sys
import xlrd
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (str(e))
# 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table(file , colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数    
    colnames = table.row_values(colnameindex)  # 某一行数据    
    a = set()
    b = set()   
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            for i in range(len(colnames)):
                a = set(row[i])
                b = a|b                         
    return b

def main():
   result = excel_table(r'D:\JAVA\workspace\test\twblg_data_20131230\例句.xls')|excel_table(r'D:\JAVA\workspace\test\twblg_data_20131230\釋義.xls')
   print(len(result))   
   print(type(result.pop()))
if __name__ == "__main__":
    main()
