from unittest.case import TestCase
from 華語對照表下載.產生閩南語國語對照表 import 資料處理
import unittest

class 華語查對應閩南語(TestCase):
	def setUp(self):
		self.資料 = 資料處理()
	def test_一些(self):
		self.assertEqual(self.資料.單詞搜尋('一些'),[{
				'華語':'一些',
				'主編號':'36', 
				'漢字':'一寡', 
				'音標':'--tsi̍t-kuá'},
			{
				'華語':'一些',
				'主編號':'10471', 
				'漢字':'寡', 
				'音標':'kuá'}
			])
	def test_一些些(self):
		self.assertEqual(self.資料.單詞搜尋('一些些'),[
			{
				'華語':'一些些', 
				'主編號':'37', 
				'漢字': '一寡仔', 
				'音標':'tsi̍t-kuá-á',
		 	}
		])
				
if __name__ == "__main__":
	unittest.main()