# -*- coding: utf-8 -*-
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from csv import DictReader
from os.path import join, abspath, dirname
import re
from sys import stderr


from 臺灣言語資料庫.欄位資訊 import 字詞


class 整理又音():

    def __init__(self):
        self._粗胚 = 文章粗胚()
        self._分析器 = 拆文分析器()
        self._轉音家私 = 轉物件音家私()
        self._譀鏡 = 物件譀鏡()

    def 得著詞條(self):
        對應表 = self.詞目總檔編號漢字對應()
        切注音 = re.compile('[/、]')  # 雙注音={('佗位','tuē、tueh')}
        with open(join(dirname(abspath(__file__)), '..', 'uni', '又音.csv')) as 檔:
            讀檔 = DictReader(檔)
            for row in 讀檔:
                優勢音 = 切注音.split(row['又音'])
                if len(優勢音) == 2:
                    混合優勢音, 偏泉優勢音 = [
                        音.strip()
                        for 音 in 優勢音]
                    漢字, 混合優勢音 = self.處理全部的漢字音標(對應表[row['主編碼']], 混合優勢音)

                    漢字, 偏泉優勢音 = self.處理全部的漢字音標(對應表[row['主編碼']], 偏泉優勢音)
                    yield {
                        '文本資料': 漢字,
                        '種類': 字詞,
                        '屬性': {'音標': 混合優勢音, '腔口': '高雄優勢腔'},
                    }
                    yield {
                        '文本資料': 漢字,
                        '種類': 字詞,
                        '屬性': {'音標': 偏泉優勢音, '腔口': '臺北優勢腔'},
                    }
                else:
                    漢字, 音標 = self.處理全部的漢字音標(對應表[row['主編碼']], row['又音'])
                    yield {
                        '文本資料': 漢字,
                        '種類': 字詞,
                        '屬性': {'音標': 音標},
                    }

    def 處理全部的漢字音標(self, 漢字, 音標):
        try:
            return self.正規化漢字音標(漢字, 音標) + ([],)
        except:
            pass
        try:
            校對漢字, 校對音標 = self.漢字音標特別格式處理(
                漢字,
                音標)
            正規化音標 = self.正規化漢字音標(
                音標, 音標
            )
            return 漢字, 正規化音標[1], [(校對漢字, 校對音標)]
        except Exception as 錯誤:
            print(錯誤, file=stderr)

    def 正規化漢字音標(self, 漢字, 音標):
        處理減號音標 = self._粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 音標)
        處理了音標 = self._粗胚.符號邊仔加空白(處理減號音標)
        原音章物件 = self._分析器.產生對齊章(漢字, 處理了音標)
        上尾章物件 = self._轉音家私.轉音(臺灣閩南語羅馬字拼音, 原音章物件)
        return self._譀鏡.看型(上尾章物件), self._譀鏡.看音(上尾章物件)

    def 漢字音標特別格式處理(self, 漢字, 音標):
        華語地名 = {
            ('蓮蕉花', 'lân-tsiau'): '蓮蕉',
        }
        合音字表 = {
            ('下昏', 'i̋ng'): '⿰下昏',
            ('下昏暗', 'ing-àm'): '⿰下昏暗',
            ('今仔', 'ta̋nn'): '⿰今仔',
            ('予伊', 'hoo'): '⿰予伊',
            ('早起時仔', 'tsái-sî-á'): '⿰早起時仔',
            ('佗位', 'tuē、tueh'): '⿰佗位',
            ('來去', 'laih'): '⿰來去',
            ('來去', 'la̋i'): '⿰來去',
            ('亞鉛鉼', 'ân-phiánn'): '⿰亞鉛鉼',
            ('亞鉛鉼', 'iân-phiánn'): '⿰亞鉛鉼',
            ('亞鉛線', 'ân-suànn'): '⿰亞鉛線',
            ('亞鉛線', 'iân-suànn'): '⿰亞鉛線',
            ('拍毋見', 'phàng-kiàn'): '⿰拍毋見',
            ('拍毋見', 'phàng-kìnn'): '⿰拍毋見',
            ('昨昏', 'tsa̋ng'): '⿰昨昏',
            ('查某𡢃', 'tsa̋u-kán'): '⿰查某𡢃',
            ('查某人', 'tsa̋u-lâng'): '⿰查某人',
            ('查某囝', 'tsa̋u-kiánn'): '⿰查某囝',
            ('查某囡仔', 'tsa̋u-gín-á'): '⿰查某囡仔',
            ('查某孫', 'tsa̋u-sun'): '⿰查某孫',
            ('查某間', 'tsa̋u-king'): '⿰查某間',
            ('差不多', 'tsha̋u-to'): '⿰差不多',
            ('啥人', 'siáng'): '⿰啥人',
            ('啥人', 'siâng'): '⿰啥人',
            ('就按呢', 'tsua̋n-ne'): '⿰就按呢',
            ('無要緊', 'bua̋-kín'): '⿰無要緊',
            ('無愛', 'buaih'): '⿰無愛',
            ('嫁查某囝', 'kè tsa̋u-kiánn'): '⿰嫁查某囝',
            ('落去', 'lueh'): '⿰落去',
            ('差不多', 'tsha̋u'): '⿰⿰差不多',
            ('就按呢', 'tsua̋n'): '⿰⿰就按呢',
            ('佗位', 'tuē'): '⿰佗位',
            ('佗位', 'tueh'): '⿰佗位',
        }
        if (漢字, 音標) in 華語地名:
            return 華語地名[(漢字, 音標)], 音標
        elif (漢字, 音標) in 合音字表:
            return 合音字表[(漢字, 音標)], 音標
        else:
            raise ValueError(
                '無處理著的漢字音標：{}、{}'.format(
                    漢字, 音標
                )
            )

    def 詞目總檔編號漢字對應(self):
        對應表 = {}
        with open(join(dirname(abspath(__file__)), '..', 'uni', '詞目總檔.csv')) as 檔:
            讀檔 = DictReader(檔)
            for row in 讀檔:
                對應表[row['主編碼']] = row['詞目']
        return 對應表
