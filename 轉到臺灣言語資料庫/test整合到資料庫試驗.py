from unittest.case import TestCase
from 轉到臺灣言語資料庫.整理詞目總檔 import 整理詞目總檔
from 轉到臺灣言語資料庫.整理又音 import 整理又音
from 轉到臺灣言語資料庫.整理方言詞 import 整理方言詞
from 轉到臺灣言語資料庫.整理例句 import 整理例句
from 轉到臺灣言語資料庫.整理外來詞 import 整理外來詞


class 整合到資料庫試驗(TestCase):

    def setUp(self):
        self.整理詞目總檔 = 整理詞目總檔()
        self.整理又音 = 整理又音()
        self.整理方言詞 = 整理方言詞()
        self.整理例句 = 整理例句()

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
                '校對': [('竹圍仔', 'tik4-ui5-a2')],
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

    def test_檢查語句類型(self):
        結果 = self.整理例句.例句類型('Âng-enn-á khàu kah tsi̍t sin-khu kuānn.')
        self.assertEqual(結果, '語句')

    def test_檢查字詞結果(self):
        結果 = self.整理例句.例句類型('tsi̍t luí hue')
        self.assertEqual(結果, '字詞')

    def test_檢查專有詞結果(self):
        結果 = self.整理例句.例句類型('Ông Tsiau-kun')
        self.assertEqual(結果, '字詞')

    def test_一般例句結果(self):
        結果 = self.整理例句.整理漢字音標(
            '若想著這層代誌，我就火大。',
            'Nā siūnn-tio̍h tsit tsân tāi-tsì, guá tō hué-tuā.'
        )
        self.assertEqual(
            結果,
            (
                '若想著這層代誌，我就火大。',
                'na7 siunn7-tioh8 tsit4 tsan5 tai7-tsi3 , gua2 to7 hue2-tua7 .',
                []
            )
        )

    def test_校對例句結果(self):
        結果 = self.整理例句.整理漢字音標(
            '伊慣勢早睏，過九點就毋通閣敲電話予伊。',
            'I kuàn-sì tsá-khùn, kuè káu tiám tō m̄-thang khà-tiān-uē hōo--i.'
        )
        self.assertEqual(
            結果,
            (
                '伊慣勢早睏，過九點就毋通閣敲電話予伊。',
                'i1 kuan3-si3 tsa2-khun3 , kue3 kau2 tiam2 to7 m7-thang1 kha3-tian7-ue7 hoo7-0i1 .',
                [
                    ('伊慣勢早睏，過九點就毋通閣敲電話予伊。',
                     'i1 kuan3-si3 tsa2-khun3 , kue3 kau2 tiam2 to7 m7-thang1 koh4 kha3-tian7-ue7 hoo7-0i1 .'
                     )
                ]
            )
        )

    def test_整理詞目總檔得著詞條檢查(self):
        for 詞條 in 整理詞目總檔().得著詞條():
            self.得著詞條檢查(詞條)

    def test_整理又音得著詞條檢查(self):
        for 詞條 in 整理又音().得著詞條():
            self.得著詞條檢查(詞條)

    def test_整理方言詞得著詞條檢查(self):
        for 詞條 in 整理方言詞().得著詞條():
            self.得著詞條檢查(詞條)

    def test_整理外來詞得著詞條檢查(self):
        for 詞條 in 整理外來詞().得著詞條():
            self.得著詞條檢查(詞條)

    def test_整理例句得著詞條檢查(self):
        for 詞條 in 整理例句().得著詞條():
            self.得著詞條檢查(詞條)

    def 得著詞條檢查(self, 詞條):
        self.assertIsInstance(詞條['文本資料'], str)
        self.assertGreater(len(詞條['文本資料']), 0)
        if '華語' in 詞條:
            self.assertIsInstance(詞條['華語'], list)
            for 華語 in 詞條['華語']:
                self.assertIsInstance(華語, str)
        if '校對' in 詞條:
            self.assertIsInstance(詞條['校對'], list)
            for 漢字, 音標 in 詞條['校對']:
                self.assertIsInstance(漢字, str)
                self.assertIsInstance(音標, str)
