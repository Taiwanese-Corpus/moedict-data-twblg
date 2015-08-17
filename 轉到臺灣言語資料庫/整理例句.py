# -*- coding: utf-8 -*-
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from csv import DictReader
from os.path import join, abspath, dirname
from sys import stderr


class 整理例句():

    無好的例 = {
        (
            '伊的豬仔，?逐隻都飼甲肥朒朒。',
            'I ê ti-á, ta̍k tsiah to tshī kah puî-tsut-tsut.'
        ):
        (
            '伊的豬仔，逐隻都飼甲肥朒朒。',
            'I ê ti-á, ta̍k tsiah to tshī kah puî-tsut-tsut.'
        ),
        (
            '日頭足炎',
            'ji̍t-thâu tsiok iām.'
        ): (
            '日頭足炎',
            'ji̍t-thâu tsiok iām'
        ),
        (
            '伊慣勢早睏，過九點就毋通閣敲電話予伊。',
            'I kuàn-sì tsá-khùn, kuè káu tiám tō m̄-thang khà-tiān-uē hōo--i.'
        ): (
            '伊慣勢早睏，過九點就毋通閣敲電話予伊。',
            'I kuàn-sì tsá-khùn, kuè káu tiám tō m̄-thang koh khà-tiān-uē hōo--i.'
        ),
        (
            '伊逐工透早攏愛啉豆奶、食包仔。',
            'I ta̍k kang thàu-tsá lóng ài lim tāu-ling tsia̍h pau-á.'
        ): (
            '伊逐工透早攏愛啉豆奶、食包仔。',
            'I ta̍k kang thàu-tsá lóng ài lim tāu-ling, tsia̍h pau-á.'
        ),

    }

    def __init__(self):
        self._粗胚 = 文章粗胚()
        self._分析器 = 拆文分析器()
        self._轉音家私 = 轉物件音家私()
        self._譀鏡 = 物件譀鏡()

    def 得著詞條(self):
        with open(join(dirname(abspath(__file__)), '..', 'uni', '例句.csv')) as 檔:
            讀檔 = DictReader(檔)
            for row in 讀檔:
                漢字 = row['例句'].strip()
                音標 = row['例句標音'].strip()
                華語 = row['華語翻譯'].strip()
                if 華語 == '':
                    華語 = 漢字
                處理漢字, 處理音標, 處理校對 = self.整理漢字音標(漢字, 音標)
                yield {
                    '文本資料': 處理漢字,
                    '種類': self.例句類型(處理音標),
                    '屬性': {'音標': 處理音標},
                    '校對': 處理校對,
                    '華語': [華語]
                }

    def 整理漢字音標(self, 漢字, 音標):
        try:
            return self.正規化漢字音標(漢字, 音標) + ([],)
        except Exception as 錯誤:
            pass
        try:
            校對漢字音標 = self.正規化漢字音標(
                *self.無好的例[(漢字, 音標)])
            正規化音標 = self.正規化音標(音標)
            return 漢字, 正規化音標, [校對漢字音標]
        except Exception as 錯誤:
            print(錯誤, 漢字, 音標, file=stderr)
            raise

    def 正規化漢字音標(self, 漢字, 音標):
        處理減號音標 = self._粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 音標)
        處理了音標 = self._粗胚.符號邊仔加空白(處理減號音標)
        原音句物件 = self._分析器.產生對齊句(漢字, 處理了音標)
        上尾句物件 = self._轉音家私.轉音(臺灣閩南語羅馬字拼音, 原音句物件)
        return self._譀鏡.看型(上尾句物件), self._譀鏡.看音(上尾句物件)

    def 正規化音標(self,  音標):
        處理減號音標 = self._粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 音標)
        處理了音標 = self._粗胚.符號邊仔加空白(處理減號音標)
        原音句物件 = self._分析器.建立句物件(處理了音標)
        上尾句物件 = self._轉音家私.轉音(臺灣閩南語羅馬字拼音, 原音句物件)
        return self._譀鏡.看型(上尾句物件, 物件分字符號='-', 物件分詞符號=' ')

    def 例句類型(self, 音標):
        if 音標[-1].isdigit():
            return '字詞'
        if 音標[-1] in '.!?"':
            return '語句'
        return '字詞'
