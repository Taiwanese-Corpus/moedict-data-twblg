from unittest.case import TestCase


from 新臺語運動.整合到資料庫 import 整合到資料庫


class 整合到資料庫試驗(TestCase):

    def setUp(self):
        self.整合 = 整合到資料庫()

    def test_一般詞目總檔(self):
        self.assertEqual(
            len(list(
                self.整合.詞目總檔(
                    主編碼=1, 屬性=1, 詞目='一', 音讀='tsi̍t'
                )
            )),
            2)

    def test_有三區詞目總檔(self):
        self.assertEqual(
            len(list(
                self.整合.詞目總檔(
                    主編碼=1, 屬性=1, 詞目='俞', 音讀='Jû/Lû/Jî'
                )
            )),
            3)
