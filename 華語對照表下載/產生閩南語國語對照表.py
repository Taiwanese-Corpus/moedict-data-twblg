import urllib.request
import xlrd
import time
from html.parser import HTMLParser
import json
import os
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs

class excel處理():
	def open_excel(self, file):
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
						b = a | b															
		return b

	def excel_table_for_編號(self, file, colnameindex=0, by_index=0):
		詞目總檔 = []
		with open(file) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				詞目總檔.append({
						'主編碼':row['主編碼'],
						'詞目':row['詞目'],
						'音讀':row['音讀']})
		return 詞目總檔


class MyHTMLParser(HTMLParser):
	# 無法度確定什麼時候會初使化，資料盡量要歸零，所以丟給main維護
	def 初使化(self):
		self.output = []
		self.counter = 0 
	def handle_data(self, data):
		self.counter += 1							
		self.output.append(data)	

			
class 資料處理():	
	def __init__(self):
		self.全部國語詞 = []
		self.國語詞集合 = set()
		self.國台字音表 = []
	
	def 單字搜尋(self, 所有字集, Word):
		for i in 所有字集:
			NextWord = urllib.request.quote(i)
			NewWord = Word + NextWord				
			url = "http://twblg.dict.edu.tw/holodict_new/searchSuggest.jsp?sample={0}&querytarget=2"\
				.format(NewWord)
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
# 						print(self.全部國語詞) 
			if parser.counter == 10:
				self.單字搜尋(所有字集, NewWord)
			self.單字搜尋(所有字集, NextWord)
	
	def 單詞搜尋(self, 華語):
		單詞 = urllib.request.quote(華語)
		urlx = \
			"http://twblg.dict.edu.tw/holodict_new/result.jsp?radiobutton=0&limit=20&querytarget=2&sample={0}&submit.x=42&submit.y=14"\
				.format(單詞)
		sock = urllib.request.urlopen(urlx)
		soup = BeautifulSoup(sock.read().decode("utf8"))
		對應閩南語資料=[]
		表 = soup.findAll('table', {'class':'shengmuTab'})
		for table in 表:
# 			print(tr,'1')
			for tr in table.findAll('tr')[1:]:
				td = tr.findAll('td')
# 				print(td[0])
				網址 = td[1].find('a').get('href')
				網址結構 = urlparse(網址)
				編號 = parse_qs(網址結構.query)['n_no'][0]
# 				print(編號)
# 				print(td[1].get_text())
# 				print(td[2].get_text())
# 				print(td[3].get_text())
				對應閩南語資料.append({
					'華語':華語, 
					'主編號':編號, 
					'漢字': td[1].get_text().strip(), 
					'音標':td[2].get_text().strip(),
					})
		return 對應閩南語資料
	
	def 編號(self, 數字對照表):
		for i in range(len(self.國台字音表)):
			for j in range(len(數字對照表)):
					if self.國台字音表[i][3] == 數字對照表[j]['音讀']:
						self.國台字音表[i][1] = 數字對照表[j]['主編號'] 
				
if __name__ == "__main__":
	這馬資料夾 = os.path.dirname(os.path.abspath(__file__))
	excel處理工具 = excel處理()
	所有字集 = ['一', '個']  # excel.excel_table_for_字元(r'../twblg_data_20131230/例句.xls')|excel.excel_table_for_字元(r'../twblg_data_20131230/釋義.xls')
	數字對照表 = excel處理工具.excel_table_for_編號(os.path.join(這馬資料夾, '..', 'raw', '詞目總檔.csv'))
	資料 = 資料處理()
	資料.單字搜尋(所有字集, '')
	for i in 資料.全部國語詞:
		資料.單詞搜尋(i)	
	資料.編號(數字對照表) 
	輸出檔 = open('結果.json', 'w')
	print(json.dumps(資料.國台字音表), file=輸出檔)
	print(json.dumps(資料.國台字音表)[:50])
	輸出檔.close()
