from unittest.case import TestCase
from 華語對照表下載.產生閩南語國語對照表 import 資料處理
import unittest

class 華語查對應閩南語(TestCase):
	def setUp(self):
		self.資料 = 資料處理()
	def test_一些(self):
		self.assertEqual(self.資料.單詞搜尋('一些'),
			[['一些', '1', '一寡', '--tsi̍t-kuá'], ['一些', '2', '寡', 'kuá']])
	def test_一些些(self):
		self.assertEqual(self.資料.單詞搜尋('一些些'),
			[['一些些', '1', '一寡仔', 'tsi̍t-kuá-á']])
				
if __name__ == "__main__":
	unittest.main()