import urllib.request
import xdrlib , sys
import xlrd
import time
from html.parser import HTMLParser

class handle_excel():
	def open_excel(self,file):
		try:
				data = xlrd.open_workbook(file)
				return data
		except Exception as e:
				print (str(e))

	def excel_table_for_字元(self, file, colnameindex=0, by_index=0):
		data = self.open_excel(file)
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

	def excel_table_for_編號(self, file, colnameindex=0, by_index=0):
		a = []	
		data = self.open_excel(file)
		table = data.sheets()[by_index]
		nrows = table.nrows# 行数	
		colnames = table.row_values(colnameindex)# 某一行数据			
		for rownum in range(1, nrows):
				row = table.row_values(rownum)
				a.append( (row[0],row[3]) )			
		return a


class MyHTMLParser(HTMLParser):
	#無法度確定什麼時候會初使化，資料盡量要歸零，所以丟給main維護
	def 初使化(self):
		self.output = []
		self.counter = 0 
	def handle_data(self, data):
		self.counter += 1							
		self.output.append(data)	

			
class 資料處理():
	excel = handle_excel()
	所有字集 = excel.excel_table_for_字元(r'../twblg_data_20131230/例句.xls')|excel.excel_table_for_字元(r'../twblg_data_20131230/釋義.xls')
	數字對照表 = excel.excel_table_for_編號(r'../twblg_data_20131230/詞目總檔(含俗諺).xls')	
	全部國語詞=[]
	國語詞集合=set()
	國台字音表=[]
	
	def 單字搜尋(self, Word = ""):
		for i in self.所有字集:
			while True:
					try:
						NextWord = urllib.request.quote(i)
					except:
						time.sleep(6)
					else:
						break
			NewWord = Word + NextWord				
			url = "http://twblg.dict.edu.tw/holodict_new/searchSuggest.jsp?sample=" + NewWord + "&querytarget=2"
			while True:
					try:
						sock = urllib.request.urlopen(url)
					except:
						time.sleep(6)
					else:
						break 
			parser = MyHTMLParser(strict=False)	
			parser.初使化()
			parser.feed(sock.read().decode("utf8").strip())
			sock.close()
			for 詞 in parser.output:
					if 詞 not in self.國語詞集合:
						self.全部國語詞.append(詞)
						self.國語詞集合.add(詞)		
						print(self.全部國語詞) 
			if parser.counter == 10:
					self.單字搜尋(NextWord)			
										
	
	def 單詞搜尋(self):
		定位a = '<tr class="all_space1">'
		定位b = '</table>'		
		for i in self.全部國語詞:			
			x = 0
			單詞 = urllib.request.quote(i)
			urlx = "http://twblg.dict.edu.tw/holodict_new/result.jsp?radiobutton=0&limit=20&querytarget=2&sample="+單詞+"&submit.x=42&submit.y=14"
			sock = urllib.request.urlopen(urlx)
			parser = MyHTMLParser(strict=False)
			parser.初使化()
			parser.output.append(i)
 
			for j in sock.read().decode("utf8").split('\n'):
					j = j.strip()			
					if j == 定位a or x >0:
						x = 1												
						parser.feed(j)
						if parser.counter == 3:
							self.國台字音表.append(parser.output)									
							parser.初使化()
							parser.output.append(i)																																					
					if j == 定位b:			
						x = 0
			sock.close()								
	
	def 編號(self):
		for i in range(len(self.國台字音表)):
			for j in range(len(self.數字對照表)):
					if self.國台字音表[i][3] == self.數字對照表[j][1]:
						self.國台字音表[i][1] = self.數字對照表[j][0]
		print(self.國台字音表) 
				
if __name__ == "__main__":
	資料 = 資料處理()
	資料.單字搜尋()			
	資料.單詞搜尋()	
	資料.編號() 


					
		
				
				
				