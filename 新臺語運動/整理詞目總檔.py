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


# from 臺灣言語資料庫.資料模型 import 來源表
# from 臺灣言語資料庫.資料模型 import 版權表
# from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 語句


class 整理詞目總檔():
    例句會當變動符號 = False
    教育部閩南語辭典空白符號 = '\u3000 \t'

    def __init__(self):
        self._粗胚 = 文章粗胚()
        self._分析器 = 拆文分析器()
        self._轉音家私 = 轉物件音家私()
        self._譀鏡 = 物件譀鏡()

    def 得著詞條(self):
        with open(join(dirname(abspath(__file__)), '..', 'uni', '詞目總檔.csv')) as 檔:
            讀檔 = DictReader(檔)
            for row in 讀檔:
                row.pop('文白')
                row.pop('部首')
                for 詞條 in self.詞目總檔(**row):
                    try:
                        self.正規化詞條音標(詞條)
                        yield 詞條
                    except Exception as 錯誤:
                        print(錯誤, 詞條, file=stderr)

    def 正規化詞條音標(self, 詞條):
        try:
            音標 = 詞條['屬性']['音標']
        except:
            return [詞條]
        漢字 = 詞條['文本資料']
        處理減號音標 = self._粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 音標)
        處理了音標 = self._粗胚.符號邊仔加空白(處理減號音標)

        try:
            原音章物件 = self._分析器.產生對齊章(漢字, 處理了音標)
            上尾章物件 = self._轉音家私.轉音(臺灣閩南語羅馬字拼音, 原音章物件)
            詞條['屬性']['音標'] = self._譀鏡.看音(上尾章物件)
            漢字 = 詞條['文本資料'] = self._譀鏡.看型(上尾章物件)
            return [詞條]
        except:
            return self.正規化詞條音標特別處理(詞條)

    def 正規化詞條音標特別處理(self, 詞條):
        音標 = 詞條['屬性']['音標']
        漢字 = 詞條['文本資料']
        華語地名 = {
            ('竹圍', 'Tik-uî-á'): '竹圍仔',
            ('石牌', 'Tsio̍h-pâi-á'): '石牌仔',
            ('拔林', 'Pa̍t-á-nâ'): '拔仔林',
            ('蓮蕉花', 'lân-tsiau'): '蓮蕉',
            ('圓山', 'Înn-suann-á'): '圓山仔',
            ('三重', 'Sann-tîng-poo'): '三重埔',
        }
        漢字漏勾 = {
            (
                '收瀾收予焦，予你生一个有',
                'Siu-nuā siu hōo ta, hōo lí senn tsi̍t ê ū lān-pha.'
            ): '收瀾收予焦，予你生一个有𡳞脬。'
        }
        雙地名 = {
            ('苓仔寮、能雅寮', 'Lîng-á-liâu'),
        }
        括號雙地名 = {
            ('竿(菅)蓁林', 'Kuann-tsin-nâ'),
        }
        雙音標 = {
            ('汐止', 'Si̍k-tsí(Si̍p-tsí)'),
        }
        毋是漢語的音標 = {  # 講毋是漢語，無愛變ian
            ('屏遮那', 'Hè-sen-ná'):
            'Hè-sian-ná'
        }
        用假名的音標 = {
            ('那卡西', 'ながし'):
            '1na1-1ka7-1si3'
        }
        漢字錯誤 = {}
        漢字錯誤.update(華語地名)
        漢字錯誤.update(漢字漏勾)
        if (漢字, 音標) in 漢字錯誤:
            詞條['文本資料'] = 漢字錯誤[(漢字, 音標)]
            return self.正規化詞條音標(詞條)
        elif (漢字, 音標) in 雙地名:
            第一個詞條, 第二個詞條 = {}, {}
            第一個詞條.update(詞條)
            第二個詞條.update(詞條)
            第一個詞條['文本資料'], 第二個詞條['文本資料'] = 漢字.split('、')
            return self.正規化詞條音標(第一個詞條) + self.正規化詞條音標(第二個詞條)
        elif (漢字, 音標) in 括號雙地名:
            第一個詞條, 第二個詞條 = {}, {}
            第一個詞條.update(詞條)
            第二個詞條.update(詞條)
            拆漢字 = re.match('(.+)\((.+)\)(.+)', 漢字)
            第一個詞條['文本資料'] = 拆漢字.group(1) + 拆漢字.group(3)
            第二個詞條['文本資料'] = 拆漢字.group(2) + 拆漢字.group(3)
            return self.正規化詞條音標(第一個詞條) + self.正規化詞條音標(第二個詞條)
        elif (漢字, 音標) in 雙音標:
            第一個詞條, 第二個詞條 = {}, {}
            第一個詞條.update(詞條)
            第二個詞條.update(詞條)
            拆音標 = re.match('(.+)\((.+)\)', 音標)
            第一個詞條['屬性']['音標'], 第二個詞條['屬性']['音標'] = 拆音標.group(1, 2)
            return self.正規化詞條音標(第一個詞條) + self.正規化詞條音標(第二個詞條)
        elif (漢字, 音標) in 毋是漢語的音標:
            詞條['屬性']['音標'] = 毋是漢語的音標[(漢字, 音標)]
            return self.正規化詞條音標(詞條)
        elif (漢字, 音標) in 用假名的音標:
            第一個詞條, 第二個詞條 = {}, {}
            第一個詞條.update(詞條)
            第二個詞條.update(詞條)
            第二個詞條['文本資料']=第二個詞條['屬性']['音標']
            第一個詞條['屬性']['音標']=用假名的音標[(漢字, 音標)]
            第二個詞條['屬性']['音標']=用假名的音標[(漢字, 音標)]
            return self.正規化詞條音標(第一個詞條) + self.正規化詞條音標(第二個詞條)
        else:
            raise

    def 詞目總檔(self, 主編碼, 屬性, 詞目, 音讀):
        if 屬性 == 25:
            種類 = 語句
        else:
            種類 = 字詞
#             if 主音 == {'Si̍k-tsí(Si̍p-tsí)'}:
#                 主音 = {'Si̍k-tsí', 'Si̍p-tsí'}
# 					if 音 == 'tsánn-tiū-á-bué/bé':
# 						音 = 'tsánn-tiū-á-bué/tsánn-tiū-á-bé'
        if 音讀 is '':
            yield {
                '文本資料': 詞目,
                '種類': 種類,
            }
        else:
            優勢音 = 音讀.split('/')
            if len(優勢音) == 1:
                混合優勢音 = 優勢音[0].strip(self.教育部閩南語辭典空白符號)
                偏泉優勢音 = 混合優勢音
            elif len(優勢音) == 2:
                混合優勢音, 偏泉優勢音 = [
                    音.strip(self.教育部閩南語辭典空白符號)
                    for 音 in 優勢音]
            else:
                for 結果 in self.三區詞目總檔(主編碼, 種類, 詞目, 音讀):
                    yield 結果
                return
            yield {
                '文本資料': 詞目,
                '種類': 種類,
                '屬性': {'音標': 混合優勢音, '腔口': '高雄優勢音'},
            }
            yield {
                '文本資料': 詞目,
                '種類': 種類,
                '屬性': {'音標': 偏泉優勢音, '腔口': '臺北優勢音'},
            }

    def 三區詞目總檔(self, 主編碼, 種類, 詞目, 音讀):
        if (詞目, 音讀) == ('俞', 'Jû/Lû/Jî'):
            return [
                {
                    '文本資料': 詞目,
                    '種類': 種類,
                    '屬性': {'音標': 'Jû', '腔口': '高雄優勢音'},
                },
                {
                    '文本資料': 詞目,
                    '種類': 種類,
                    '屬性': {'音標': 'Lû', '腔口': '高雄優勢音'},
                },
                {
                    '文本資料': 詞目,
                    '種類': 種類,
                    '屬性': {'音標': 'Jî', '腔口': '臺北優勢音'},
                }]
        raise RuntimeError('音讀不只兩區：{}'.format(音讀))

# 					if 音 == 'ke/kue-tshíng' and 主編號 == 12744 and len(主音) > 1:
# 						continue
#                 else:

#             if len(方言差) == 6:
#                 # "主編號"=12239
#                 字方言差 = list(揣字方言差(方言差)[0])[3:]
#                 for i in range(len(字方言差欄位)):
#                     字方言差[i] = 字方言差[i].strip()
#                     if 字方言差[i] != 'x' and 字方言差[i] != '暫無資料':
#                         # 						print(字方言差[i])
#                         # 							if 字方言差[i] == 'tshiòr/tshiònn':
#                         # 								字方言差[i] = 'tshiòr;tshiònn'
#                         腔口集[字方言差欄位[i]] = {}
#                         腔口集[字方言差欄位[i]][漢字] = [
#                             方言.strip(教育部閩南語辭典空白符號) for 方言 in 字方言差[i].split(';')]
#             elif len(方言差) == 8:
#                 # "主編號"=4368
#                 詞方言差 = list(揣詞方言差(方言差)[0])[3:]
#                 for i in range(len(詞方言差欄位)):
#                     詞方言差[i] = 詞方言差[i].strip()
#                     if 詞方言差[i] != 'x' and 詞方言差[i] != '暫無資料':
#                         # 						print(詞方言差[i])
#                         # 							if 詞方言差[i] == '菅芒　kuann-bang, kuann-bâng':
#                         # 								詞方言差[i] = '菅芒　kuann-bang; kuann-bâng'
#                         # 							elif 主編號 == 2876:
#                         # 								詞方言差[i] = 詞方言差[i].replace('tuē', 'tuē; tueh')
#                         # 							elif 詞方言差[i] == '秤砣　tshìn-thô(tô)':
#                         # 								詞方言差[i] = '秤砣　tshìn-thô;tshìn-tô'
#
#                         字音集 = [一組字音.split(教育部閩南語辭典隔開符號, 1)
#                                for 一組字音 in 詞方言差[i].split(',')]
#                         字音對照 = {}
#                         for 字, 音 in 字音集:
#                             字音對照[字.strip(教育部閩南語辭典空白符號)] = [
#                                 資料.strip(教育部閩南語辭典空白符號) for 資料 in 音.split(';')]
#                         腔口集[詞方言差欄位[i]] = 字音對照

#             編修物件集 = []
#             for 腔口, 字音 in 腔口集.items():
#                 for 字, 音集 in 字音.items():
#                     原本音流水號集 = []
#                     俗音流水號集 = []
#                     合音流水號集 = []
#                     組字式型體 = 辭典工具.共造字換做統一碼表示法(字)
#                     # 資料型體 = 粗胚.符號邊仔加空白(資料型體).strip()
#                     for 音 in 音集:
#                         # 有人會改，愛備份
#                         資料型體 = 組字式型體
#
#                         是俗音 = False
#                         是合音 = False
# # 							if 資料型體 == '熟' and 音 == 'tînn-kha-puānn-tshiú':
# # 								continue
#                         if 音 == 'iang35-ua55-ua55':
#                             continue
#                         資料型體, 音 = self.語句調整(主編號, 資料型體, 音)
#
#
#                         if 音.endswith(俗音記號):
#                             是俗音 = True
#                             音 = 音[:-len(俗音記號)]
#                         elif 音.endswith(合音記號):
#                             音 = 音[:-len(合音記號)]
#                         合音字表 = {('下昏暗', 'ing-àm'), ('下昏暗時', 'ing-àm-sî'), ('下昏時', 'ing-sî'),
#                                 ('下昏', 'i̋ng'), ('這陣',
#                                                  'tsín'), ('這陣', 'tsún'),
#                                 ('佗位', 'tuē'), ('佗位',
#                                                 'tueh'), ('嘿啦', 'hiàu'),
#                                 ('查某𡢃', 'tsőo-kán'), ('查某𡢃仔',
#                                                        'tsőo-kán-á'),
#                                 ('查某囡仔', 'tsa̋-gín-á'), ('查某囡仔',
#                                                          'tsa̋u-gín-á'),
#                                 ('查某孫', 'tsa̋u-sun'),
#                                 ('啥物人', 'siàng-n̂g'), ('啥物人', 'sáng-n̂g'), }
#                         if  (資料型體 in 腔口集[偏漳優勢音腔口] and (音 + 合音記號) in 腔口集[偏漳優勢音腔口][資料型體]) or \
#                                 ((資料型體, 音) in 合音字表):
#                             是合音 = True
#                         if 是合音:
#                             if 主編號 == 9440:  # 嫁查甫囝
#                                 資料型體 = 資料型體[:1] + '⿰' + 資料型體[1:]
#                             # tsua̋n
#                             elif 主編號 == 8331 and '-' not in 音:
#                                 資料型體 = '⿰⿰' + 資料型體
#                             # tsha̋u
#                             elif 主編號 == 5923 and '-' not in 音:
#                                 資料型體 = '⿰⿰' + 資料型體
#                             else:
#                                 資料型體 = '⿰' + 資料型體
#                         第二三字組合 = {('硩落去', 'teh--loih'), ('硩落去', 'teh--loì'),
#                                   ('嫁查某囝', 'kè-tsőo-kiánn'), ('嫁查某囝',
#                                                                'kè-tsa̋u-kiánn'),
#                                   ('嫁查某囝', 'kè-tsőo-kiánn'), ('嫁查某囝',
#                                                                'kè-tsa̋u-kánn'),
#                                   }
#                         if ((資料型體, 音) in 第二三字組合):
#                             資料型體 = 資料型體[:1] + '⿰' + 資料型體[1:]
#                         if (資料型體, 音) in {('阮厝的查某人', 'gún-tshù-ê-tsa̋u-lâng')}:
#                             資料型體 = 資料型體.replace('查某', '⿰查某')
#
#                         資料型體, 音 = self.日語處理(主編號, 資料型體, 音)
#
#                         音 = 粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 音)
#                         音 = 粗胚.符號邊仔加空白(音).strip()
#                         地區對應 = {'鹿港': 偏泉優勢音腔口, '三峽': 偏泉優勢音腔口, '臺北': 偏泉優勢音腔口,
#                                 '宜蘭': 偏漳優勢音腔口, '臺南': 混合優勢音腔口, '高雄': 混合優勢音腔口, '金門': 偏泉優勢音腔口,
#                                 '馬公': 偏泉優勢音腔口, '新竹': 偏泉優勢音腔口, '臺中': 偏漳優勢音腔口, }
#                         所在地區 = 教育部閩南語辭典地區
#                         for 對應地區, 對應腔口 in 地區對應.items():
#                             if 對應地區 in 腔口:
#                                 腔口 = 對應腔口
#                                 所在地區 = 對應地區
#                         if 腔口 not in {偏泉優勢音腔口, 偏漳優勢音腔口, 混合優勢音腔口}:
#                             raise RuntimeError('腔口無著！！{0}'.format(腔口))
# # 						if True:
#                         try:
#                             原音句物件 = 分析器.產生對齊句(資料型體, 音)
#                             上尾句物件 = 轉音家私.轉做標準音標(臺灣閩南語羅馬字拼音, 原音句物件)
#                             if self.加入文字:
#                                 文字物件 = 文字.objects.create(來源=教育部閩南語辭典名,
#                                                          種類=種類, 腔口=腔口, 地區=所在地區, 年代=教育部閩南語辭典年代,
#                                                          型體=譀鏡.看型(上尾句物件), 音標=譀鏡.看音(上尾句物件))
#                                 編修物件 = 文字物件.流水號
#                                 編修物件集.append(編修物件)
#                                 教育部臺灣閩南語常用詞辭典來源.objects.create(
#                                     流水號=編修物件, 主編號=主編號)
#                                 if 是俗音:
#                                     俗音流水號集.append(編修物件)
#                                 elif 是合音:
#                                     合音流水號集.append(編修物件)
#                                 else:
#                                     原本音流水號集.append(編修物件)
#                         except Exception as 錯誤:
#                             print(
#                                 '主編號', 主編號, 譀鏡.看型(上尾句物件), 譀鏡.看音(上尾句物件), 錯誤)
#                             raise 錯誤

    def 語句調整(self, 主編號, 資料型體, 音):
        if 音 == "sai-kong-á (面稱)":
            音 = "sai-kong-á"
        elif 音 == "sai-sun-á (背稱)":
            音 = "sai-sun-á"
        elif 音 == "khioh-gín-á(產婆語)":
            音 = "khioh-gín-á"
        elif 音 == "tshâ-se(大)":
            音 = "tshâ-se"
        elif 音 == "luai̍h-á(小)":
            音 = "luai̍h-á"
        elif 音 == "hông-hun(書)":
            音 = "hông-hun"
        elif 音 == 'tsînn(中間有孔)':
            音 = 'tsînn'  # 鐳　lui (無空的)
        elif 音 == 'tshâ-se(大)':
            音 = 'tshâ-se'
        elif 音 == 'luai̍h-á(小)':
            音 = 'luai̍h-á'
        elif 音 == 'guán(男)':
            音 = 'guán'
        elif 音 == 'gún(女)':
            音 = 'gún'
        if 資料型體 == "司孫(背稱)":
            資料型體 = "司孫"

        elif 資料型體 == 'xx姊仔' and 音 == 'xxtsé--á':  # xx是會當換做名詞
            資料型體 = '姊仔'
            音 = 'tsé--á'
# 						elif 資料型體 == "瘦田" and 主編號 == 60344:
# 							資料型體 = "瘦田𠢕欶水。"
# 						elif 資料型體 == "䆀猴" and 主編號 == 60373:
# 							資料型體 = "䆀猴𠢕欠數。"
        # m7 tioh8
        # if 音 == "niàu-ka-tsiah hit- ki":
        # 	# love you~
        # 	音 = "niàu-ka-tsiah hit-ki"
        return 資料型體, 音

    def 日語處理(self, 主編號, 資料型體, 音):
        if (主編號, 資料型體) in self.日語替換:
            資料型體 = self.日語替換[(主編號, 資料型體)]
            音 = 音.replace('33', '7')
            音 = 音.replace('55', '1')
            音 = 音.replace('11', '3')
            音 = 音.replace('51', '2')
            音 = 音.replace('35', '5')
            音 = 音.replace('t5', 't8')
            音 = 音.replace('t3', 't4')
            音 = 音.replace('h5', 'h8')
            音 = 音.replace('h3', 'h4')
            音 = '1' + 音.replace('-', '-1')
        return 資料型體, 音
    日語替換 = {
        (10740, 'ロ—ス'): '⿰ロ—ス',
        (1114, 'メンス'): '⿰メンス',
        (1632, 'はしか'): 'はしか',
        (1736, 'ブラジゃ—'): 'ブラ⿰⿰ジャ—',
        (1736, 'ブラジャ—'): 'ブラ⿰⿰ジャ—',
        (2041, 'ステンレス'): 'ス⿰テンレス',
        (2572, 'レコード'): 'レ⿰コード',
        (2731, 'じどうしゃ'): 'じ⿰どう⿰しゃ',
        (2993, 'じしゃく'): 'じ⿰しゃく',
        (3085, 'おニンギョウ'): 'お⿰ニン⿰⿰ギョウ',
        (3085, 'オニンギョウ'): 'オ⿰ニン⿰⿰ギョウ',
        (3087, 'まんが'): '⿰まんが',
        (3436, 'ロ—ス'): '⿰ロ—ス',
        (3524, 'みそしる'): 'みそしる',
        (3524, 'みそ'): 'みそ',
        (4467, 'わさび'): 'わさび',
        (4574, 'とうさん'): '⿰とう⿰さん',
        (5106, 'トマト'): 'トマト',
        (5437, 'にんじん'): '⿰にん⿰じん',
        (6043, 'ホテル'): 'ホテル',
        (6088, 'ホテル'): 'ホテル',
        (6590, 'ガラ油'): 'ガラ油',
        (6848, 'ミシン'): 'ミ⿰シン',
        (7561, 'スリッパ'): 'ス⿰リッパ',
        (7561, 'ぞうり仔'): '⿰ぞうり仔',
        (8124, 'ビル'): 'ビル',
        (8124, 'ビ—ル'): '⿰ビ—ル',
        (8164, 'パチンコ'): 'パ⿰チンコ',
        (8727, 'ガラ油'): 'ガラ油',
        (9928, 'コレラ'): 'コレラ',
        (10927, 'アルミ'): 'アルミ',
        (10965, 'ネクタイ'): 'ネク⿰タイ',
        (11252, 'ロ—ス'): '⿰ロ—ス',
        (11988, 'ステンレス'): 'ス⿰テンレス',
        (12555, 'はしか'): 'はしか',
        (13055, 'りんご'): '⿰りんご',
        (13091, 'パン'): '⿰パン',
        # (25750, 'ながし'):'ながし',
        (7906, '鳶'): '⿰とんび',
    }
