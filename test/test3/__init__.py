import urllib.request
import xdrlib , sys
import xlrd
from html.parser import HTMLParser

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (str(e))

def excel_table(file , colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows 
    colnames = table.row_values(colnameindex)  
    a = set()
    b = set()   
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            for i in range(len(colnames)):
                a = set(row[i])
                b = a|b                                              
    return b


class MyHTMLParser(HTMLParser):
    #無法度確定什麼時候會初使化，資料盡量要歸零，所以丟給main維護
    def 初使化(self):
        self.output = []
        self.counter = 0 
    def handle_data(self, data):
        self.counter += 1                      
        self.output.append(data)    

           
def main():
   result = excel_table(r'../twblg_data_20131230/例句.xls')|excel_table(r'../twblg_data_20131230/釋義.xls')    
   全部國語詞=[]
   國語詞集合=set()
   for i in result:      
       FirstWord = urllib.request.quote(i)        
       urlx = "http://twblg.dict.edu.tw/holodict_new/searchSuggest.jsp?sample="+FirstWord+"&querytarget=2"
       sock = urllib.request.urlopen(urlx)
       parser = MyHTMLParser(strict=False)     
       parser.初使化()
       parser.feed(sock.read().decode("utf8").strip())
       for 詞 in parser.output:
           if 詞 not in 國語詞集合:
               全部國語詞.append(詞)
               國語詞集合.add(詞)
               print(全部國語詞)
       
       if parser.counter == 10:
           for j in result:
               SecondWord = urllib.request.quote(j)                
               urlx = "http://twblg.dict.edu.tw/holodict_new/searchSuggest.jsp?sample="+FirstWord+SecondWord+"&querytarget=2"
               sock = urllib.request.urlopen(urlx)
               parser = MyHTMLParser(strict=False)
               parser.初使化()
               parser.feed(sock.read().decode("utf8").strip())
               for 詞 in parser.output:
                   if 詞 not in 國語詞集合:
                       全部國語詞.append(詞)
                       國語詞集合.add(詞)
                       print(全部國語詞)
                             
 
   print("done")
            
if __name__ == "__main__":
    main()          




            
        
            
            
            