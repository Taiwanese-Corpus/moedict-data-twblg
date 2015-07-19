from unittest.case import TestCase
from 新臺語運動.整理詞目總檔 import 整理詞目總檔




class 整合到資料庫試驗(TestCase):

    def setUp(self):
        self.整理詞目總檔 = 整理詞目總檔()

    def test_一般詞目總檔(self):
        self.assertEqual(
            len(list(
                self.整理詞目總檔.詞目總檔(
                    主編碼=1, 屬性=1, 詞目='一', 音讀='tsi̍t'
                )
            )),
            1)

    def test_有腔口詞目總檔(self):
        self.assertEqual(
            len(list(
                self.整理詞目總檔.詞目總檔(
                    主編碼=1, 屬性=1, 詞目='火雞', 音讀='hué-ke/hé-kue'
                )
            )),
            2)

    def test_有三區詞目總檔(self):
        self.assertEqual(
            len(list(
                self.整理詞目總檔.詞目總檔(
                    主編碼=1, 屬性=1, 詞目='俞', 音讀='Jû/Lû/Jî'
                )
            )),
            3)
