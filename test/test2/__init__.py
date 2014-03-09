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
def excel_table2(file , colnameindex=0, by_index=0):
    數字對照表 = []    
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数    
    colnames = table.row_values(colnameindex)  # 某一行数据          
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        數字對照表.append(row[0])        
        數字對照表.append(row[3])           
    return 數字對照表

def main():
   數字對照表 = excel_table2(r'../twblg_data_20131230/詞目總檔(含俗諺).xls')
   x =[['其:', '1', '其', 'kî'], ['其中:', '1', '其中', 'kî-tiong'], ['其他:', '1', '其他', 'kî-thann'], ['其他地方:', '1', '別搭', 'pa̍t-tah'], ['其他地方:', '2', '別位', 'pa̍t-uī'], ['其實:', '1', '其實', 'kî-si̍t'], ['其次:', '1', '其次', 'kî-tshù']]   
   for i in range(len(x)):
       for j in range(len(數字對照表)):
           if x[i][3] == 數字對照表[j]:
               x[i][1] = 數字對照表[j-1]
   print(x)
       
    
if __name__ == "__main__":
    main()
