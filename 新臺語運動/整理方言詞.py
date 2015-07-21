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
#             if (資料型體, 音) in {('阮厝的查某人', 'gún-tshù-ê-tsa̋u-lâng')}:
#                 資料型體 = 資料型體.replace('查某', '⿰查某')


class 整理方言詞():

    def __init__(self):
        self._粗胚 = 文章粗胚()
        self._分析器 = 拆文分析器()
        self._轉音家私 = 轉物件音家私()
        self._譀鏡 = 物件譀鏡()

    def 得著詞條(self):
        提掉括號 = re.compile('\(.+\)')
        with open(join(dirname(abspath(__file__)), '..', 'uni', '詞彙方言差.csv')) as 檔:
            讀檔 = DictReader(檔)
            for 詞條 in 讀檔:
                #                 操他媽(詈語)
                #                 土缸、醃缸
                華語 = 提掉括號.sub('', 詞條.pop('詞目')).split('、')
                詞條.pop('流水號')
                詞條.pop('資料編號')
                for 結果 in self.提著全部的腔口(詞條):
                    結果['華語'] = 華語
                    yield 結果
        return

    def 提著全部的腔口(self, 詞條):
        for 腔, 方言音 in 詞條.items():
            if 方言音.strip() not in ['x', '暫無資料']:
                for 音 in 方言音.strip().split(','):
                    漢字, 音標組 = 音.strip().split('\u3000')
                    for 音標 in 音標組.split(';'):
                        for 字, 音, 校對 in self.處理全部的漢字音標(漢字, 音標.strip()):
                            yield {
                                '文本資料': 字,
                                '種類': 字詞,
                                '屬性': {'音標': 音, '腔口': 腔 + '腔'},
                                '校對': 校對
                            }
        return
#                 }

    def 處理全部的漢字音標(self, 漢字, 音標):
        if self.是特別漢字音標(漢字, 音標.strip()):
            for 字, 音 in self.拆特別漢字音標(漢字, 音標.strip()):
                yield self.正規化漢字音標(字, 音) + ([],)
            return
        try:
            yield self.正規化漢字音標(漢字, 音標.strip()) + ([],)
            return
        except:
            pass
        try:
            校對漢字, 校對音標 = self.漢字音標特別格式處理(
                漢字,
                音標.strip()
            )
            if 校對音標:
                上尾漢字, 上尾音標 = self.正規化漢字音標(校對漢字, 校對音標)
            else:
                上尾漢字, 上尾音標 = 校對漢字, 校對音標
            正規化音標 = self.正規化音標(
                音標
            )

            yield 漢字, 正規化音標[1], [(上尾漢字, 上尾音標)]
        except Exception as 錯誤:
            print(漢字, 音標, 錯誤, file=stderr)
#             raise
            pass

    def 正規化漢字音標(self, 漢字, 音標):
        處理減號音標 = self._粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 音標)
        處理了音標 = self._粗胚.符號邊仔加空白(處理減號音標)
        原音章物件 = self._分析器.產生對齊章(漢字, 處理了音標)
        上尾章物件 = self._轉音家私.轉音(臺灣閩南語羅馬字拼音, 原音章物件)
        return self._譀鏡.看型(上尾章物件), self._譀鏡.看音(上尾章物件)

    def 漢字音標特別格式處理(self, 漢字, 音標):
        有解釋字 = {"司孫(背稱)"}
        有解釋音 = {
            "sai-kong-á (面稱)",
            "sai-sun-á (背稱)",
            "khioh-gín-á(產婆語)",
            "tshâ-se(大)",
            "luai̍h-á(小)",
            "hông-hun(書)",
            'tsînn(中間有孔)',  # 鐳　lui (無空的)
            'tshâ-se(大)',
            'luai̍h-á(小)',
            'guán(男)',
            'gún(女)',
        }
        合音字表 = {
            ('硩落去', 'teh--loih'): '硩⿰落去',
            ('硩落去', 'teh--loì'): '硩⿰落去',
            ('昨昏', 'tsa̋ng'): '⿰昨昏',
            ('下昏暗時', 'ing-àm-sî'): '⿰下昏暗時',
            ('下昏暗', 'ing-àm'): '⿰下昏暗',
            ('下昏', 'i̋ng'): '⿰下昏',
            ('下昏時', 'ing-sî'): '⿰下昏時',
            ('佗位', 'tuē'): '⿰佗位',
            ('佗位', 'tueh'): '⿰佗位',
            ('查某囝', 'tsa̋u-kiánn'): '⿰查某囝',
            ('查某囝', 'tsa̋u-kánn'): '⿰查某囝',
            ('查某囝', 'tsőo-kiánn'): '⿰查某囝',
            ('阮厝的查某人', 'gún-tshù-ê-tsa̋u-lâng'): '阮厝的⿰查某人',
            ('嫁查某囝', 'kè-tsa̋u-kiánn'): '嫁⿰查某囝',
            ('嫁查某囝', 'kè-tsa̋u-kánn'): '嫁⿰查某囝',
            ('嫁查某囝', 'kè-tsőo-kiánn'): '嫁⿰查某囝',
            ('予人招', 'hőng-tsio'): '⿰予人招',
            ('予人招的', 'hông-tsio--ê'): '⿰予人招的',
            ('予人招', 'hông-tsio'): '⿰予人招',
            ('去予人招', 'khù-hông-tsio'): '去⿰予人招',
            ('查某𡢃', 'tsa̋u-kán'): '⿰查某𡢃',
            ('查某𡢃', 'tsa̋u-kán'): '⿰查某𡢃',
            ('查某𡢃仔', 'tsőo-kán-á'): '⿰查某𡢃仔',
            ('查某𡢃', 'tsőo-kán'): '⿰查某𡢃',
            ('查某囡仔', 'tsa̋u-gín-á'): '⿰查某囡仔',
            ('查某囡仔', 'tsa̋-gín-á'): '⿰查某囡仔',
            ('這陣', 'tsún'): '⿰這陣',
            ('這陣', 'tsín'): '⿰這陣',
            ('嘿啦', 'hiàu'): '⿰嘿啦',
            ('啥物人', 'sáng-n̂g'): '⿰啥物人',
            ('啥物人', 'siàng-n̂g'): '⿰啥物人',
        }
        # ('呱呱','ua̋k-ua̋k'):'呱呱',
        錯誤音標 = {
            ('起凊瘼', 'khí-tshìn-mo̍nnh'): 'khí-tshìn-mo̍h'
        }
        if 漢字 in 有解釋字:
            return 漢字.split('(')[0].strip(), 音標
        elif 音標 in 有解釋音:
            return 漢字, 音標.split('(')[0].strip()
        elif (漢字, 音標) in 合音字表:
            return 合音字表[(漢字, 音標)], 音標
        elif (漢字, 音標) in self.華語替換:
            return 漢字, self.正規化音標(音標)
        elif (漢字, 音標) in self.日語替換:
            return self.正規化音標(音標), ''
        elif (漢字, 音標) in 錯誤音標:
            return 漢字, 錯誤音標[(漢字, 音標)]
        elif 音標.endswith('......'):
            return 漢字, 音標.rstrip('.')
        elif 漢字.endswith(''):
            return 漢字.rstrip(''), 音標
        elif 漢字.startswith('xx') and 音標.startswith('xx'):
            return 漢字.strip('x'), 音標.strip('x')
        elif 音標.endswith('......'):
            return 漢字, 音標.rstrip('.')
        raise RuntimeError('無改著：{}、{}'.format(漢字, 音標))

    def 是特別漢字音標(self, 漢字, 音標):
        return (漢字, 音標) in [
            ('(透)中晝', '(thàu)-tiong-tàu'),
            ('透中晝(心)', 'thàu-tiong-tàu-(sim)'),
            ('秤砣', 'tshìn-thô(tô)')
        ]

    def 拆特別漢字音標(self, 漢字, 音標):
        if (漢字, 音標) == ('(透)中晝', '(thàu)-tiong-tàu'):
            return [
                ('中晝', 'tiong-tàu'),
                ('透中晝', 'thàu-tiong-tàu')
            ]
        if (漢字, 音標) == ('透中晝(心)', 'thàu-tiong-tàu-(sim)'):
            return [
                ('透中晝', 'thàu-tiong-tàu'),
                ('透中晝心', 'thàu-tiong-tàu-sim')
            ]
        if (漢字, 音標) == ('秤砣', 'tshìn-thô(tô)'):
            return [
                ('秤砣', 'tshìn-thô'),
                ('秤砣', 'tshìn-tô')
            ]

    def 語句調整(self, 主編號, 資料型體, 音):
        if 資料型體 == 'xx姊仔' and 音 == 'xxtsé--á':  # xx是會當換做名詞
            資料型體 = '姊仔'
            音 = 'tsé--á'
#                         elif 資料型體 == "瘦田" and 主編號 == 60344:
#                             資料型體 = "瘦田𠢕欶水。"
#                         elif 資料型體 == "䆀猴" and 主編號 == 60373:
#                             資料型體 = "䆀猴𠢕欠數。"
        # m7 tioh8
        # if 音 == "niàu-ka-tsiah hit- ki":
        #     # love you~
        #     音 = "niàu-ka-tsiah hit-ki"
        return 資料型體, 音

    def 正規化音標(self, 音):
        處理減號音標 = self._粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 音)
        處理了音標 = self._粗胚.符號邊仔加空白(處理減號音標)
        原音組物件 = self._分析器.建立組物件(處理了音標)
        上尾組物件 = self._轉音家私.轉音(臺灣閩南語羅馬字拼音, 原音組物件)
        return self._譀鏡.看型(上尾組物件, 物件分字符號='-')
    華語替換 = {
        ('洋娃娃', 'iang35-ua55-ua55'),
        ('瀑布', 'phu51-pu51'),
        ('拉鍊', 'la55-lian51'),
    }
    日語替換 = {
        ('アルミ', 'a33-lu55-mih3'),
        ('まんが', 'bang51-ga11'),
        ('ビル', 'bi51-lu11'),
        ('ビ—ル', 'bi51-lu11'),
        ('みそ', 'bi55-sooh3'),
        ('ブラジゃ—', 'bu33-la51-jia11'),
        ('ブラジャ—', 'bu33-la55-tsia11'),
        ('じどうしゃ', 'gi33-loo51-sia11'),
        ('はしか', 'ha33-si55-khah3'),
        ('ホテル', 'hoo33-te55-luh3'),
        ('じどうしゃ', 'ji33-lo51-sia11'),
        ('じどうしゃ', 'ji33-loo51-sia11'),
        ('じしゃく', 'ji33-sia55-kuh3'),
        ('にんじん', 'jin33-jin13'),
        ('にんじん', 'jin35-jin51'),
        ('コレラ', 'khoo33-le55-lah3'),
        ('レコード', 'le33-khoo51-too11'),
        ('じどうしゃ', 'li33-lo51-sia11'),
        ('にんじん', 'lin35-jin51'),
        ('にんじん', 'lin35-tsin51'),
        ('りんご', 'lin51-goo11'),
        ('ロ—ス', 'loo51-sir11'),
        ('ロ—ス', 'loo51-su11'),
        ('メンス', 'me51-su11'),
        ('ミシン', 'mi33-sin51'),
        ('みそしる', 'mi33-so55-si55-luh3'),
        ('みそ', 'mi55-soh3'),
        ('みそ', 'mi55-sooh3'),
        ('ネクタイ', 'ne33-kut5-tai51'),
        ('おニンギョウ', 'o33-lin55-gio5'),
        ('おニンギョウ', 'o33-lin55-gio51'),
        ('オニンギョウ', 'o33-lin55-gioh5'),
        ('パチンコ', 'pha33-tshin51-ko11'),
        ('パン', 'pháng'),
        ('スリッパ', 'sir33-li55-pah3'),
        ('スリッパ', 'sir33-lit5-pah3'),
        ('ステンレス', 'sir33-tian55-le51-sir11'),
        ('スリッパ', 'su33-li55-pah3'),
        ('トマト', 'thoo33-ma55-tooh3'),
        ('とうさん', 'too51-sang11'),
        ('わさび', 'ua33-sa55-bih3'),
        ('ぞうり仔', 'lo55-li55-a51'),
        ('ガラ油', 'gat5-la55-iû'),
        ('鳶', 'thong51-bi11'),
        ('ガス', 'ga55-suh3'),
        ('ガス', 'ga55 suh3'),
        ('バス', 'ba55-sirh3'),
        ('ロ—ス肉', 'loo55-su55-bah'),
        ('ロ—ス肉', 'loo51-su51 bah'),
        ('おかあさん', 'oo33-kha51-sang11'),
        ('オニンギョウ', 'o33-lin55-gio51'),
        ('かあさん', 'kha51-sang11'),
        ('れんたん', 'lian35-tang51'),
        ('ガソリン', 'ga33-soo55-lin51'),
        ('へルメット', 'he33-nu55-miat5-tooh3'),
        ('チャック', 'jia55-kuh3'),
        ('チャック', 'jiak5-khuh3'),
        ('チャック', 'jia55-khuh3'),
        ('チャック', 'jiak5-kuh3'),
        ('チャック', 'tsiak5-kuh3'),
        ('チャック', 'jiak5-kuh3'),
        ('チャック', 'tsiak5-kuh3'),
        ('じゃんけん', 'jiang55-kian55-pho51-sirh3'),
        ('風呂', 'hu55-looh3'),
        ('風呂', 'hu55-loh3'),
        ('風呂桶', 'hu55-lo55-tháng'),
        ('風呂桶', 'hu55-loo55-tháng'),
        ('瀧', 'tha55-khih3'),
        ('簞笥', 'thang51-su11'),
        ('簞笥', 'thang51-sirh3'),
        ('簞笥', 'thang51-suh3'),
    }
