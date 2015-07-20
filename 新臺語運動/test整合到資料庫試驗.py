from unittest.case import TestCase
from 新臺語運動.整理詞目總檔 import 整理詞目總檔
from 新臺語運動.整理又音 import 整理又音
from 新臺語運動.整理方言詞 import 整理方言詞


class 整合到資料庫試驗(TestCase):

    def setUp(self):
        self.整理詞目總檔 = 整理詞目總檔()
        self.整理又音 = 整理又音()
        self.整理方言詞 = 整理方言詞()

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

    def test_一般詞目總檔結果(self):
        self.assertEqual(
            self.整理詞目總檔.正規化詞條音標({
                '主編碼': 1,
                '文本資料': '一',
                '種類': '字詞',
                '屬性': {'音標': 'tsi̍t'},
            }),
            {
                '主編碼': 1,
                '文本資料': '一',
                '種類': '字詞',
                '屬性': {'音標': 'tsit8'},
            }
        )

    def test_有改詞目總檔結果(self):
        self.assertEqual(
            self.整理詞目總檔.正規化詞條音標({
                '主編碼': 123,
                '文本資料': '竹圍',
                '種類': '字詞',
                '屬性': {'音標': 'Tik-uî-á'},
            }),
            {
                '主編碼': 123,
                '文本資料': '竹圍',
                '種類': '字詞',
                '屬性': {'音標': 'tik4-ui5-a2'},
                '校對': [{
                    '文本資料': '竹圍仔',
                    '種類': '字詞',
                    '屬性': {'音標': 'tik4-ui5-a2'},
                }]
            }
        )

    def test_日語詞目總檔結果(self):
        self.assertEqual(
            self.整理詞目總檔.正規化詞條音標({
                '主編碼': 31001,
                '文本資料': 'a33 lu55 mih3',
                '種類': '字詞',
            }),
            None
        )

    def test_一般又音結果(self):
        漢字, 音標, 校對 = self.整理又音.處理全部的漢字音標('一觸久仔', 'tsi̍t-táu-kú-á')
        self.assertEqual(漢字, '一觸久仔')
        self.assertEqual(音標, 'tsit8-tau2-ku2-a2')
        self.assertEqual(校對, [])

    def test_有改又音結果(self):
        漢字, 音標, 校對 = self.整理又音.處理全部的漢字音標('蓮蕉花', 'lân-tsiau')
        self.assertEqual(漢字, '蓮蕉花')
        self.assertEqual(音標, 'lan5-tsiau1')
        self.assertEqual(校對, [('蓮蕉', 'lan5-tsiau1')])

    def test_一般方言結果(self):
        結果 = self.整理方言詞.處理全部的漢字音標('干樂', 'kan-lo̍k')
        漢字, 音標, 校對 = list(結果)[0]
        self.assertEqual(漢字, '干樂')
        self.assertEqual(音標, 'kan1-lok8')
        self.assertEqual(校對, [])

    def test_有改方言結果(self):
        結果 = self.整理方言詞.處理全部的漢字音標('查某囡仔', 'tsa̋u-gín-á')
        漢字, 音標, 校對 = list(結果)[0]
        self.assertEqual(漢字, '查某囡仔')
        self.assertEqual(音標, 'tsau9-gin2-a2')
        self.assertEqual(校對, [('⿰查某囡仔', 'tsau9-gin2-a2')])
