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
    Output = []
    counter = 0           
    def handle_data(self, data):                                        
        
        self.counter += 1                  
        print(self.counter)        
        self.Output.append(data)
        final = list(set(self.Output))
        final.sort(key = self.Output.index)   
        print(final)              
        
             
           
def main():
   result = excel_table(r'D:\JAVA\workspace\test\twblg_data_20131230\例句.xls')|excel_table(r'D:\JAVA\workspace\test\twblg_data_20131230\釋義.xls')    
   counter = 0
   
   for i in range(len(result)):      
       FirstWord = urllib.request.quote(result.pop())        
       urlx = "http://twblg.dict.edu.tw/holodict_new/searchSuggest.jsp?sample="+FirstWord+"&querytarget=2"
       sock = urllib.request.urlopen(urlx)
       parser = MyHTMLParser(strict=False)     
       parser.feed(sock.read().decode("utf8").strip())
           
       if parser.counter == 10:
           temp = excel_table(r'D:\JAVA\workspace\test\twblg_data_20131230\例句.xls')|excel_table(r'D:\JAVA\workspace\test\twblg_data_20131230\釋義.xls')                            
           
           for i in range(len(temp)):
               SecondWord = urllib.request.quote(temp.pop())                
               urlx = "http://twblg.dict.edu.tw/holodict_new/searchSuggest.jsp?sample="+FirstWord+SecondWord+"&querytarget=2"
               print(urlx)
               sock = urllib.request.urlopen(urlx)
               parser = MyHTMLParser(strict=False)
               parser.feed(sock.read().decode("utf8").strip())
                             
 
   print("done")
            
if __name__ == "__main__":
    main()          




            
        
            
            
            