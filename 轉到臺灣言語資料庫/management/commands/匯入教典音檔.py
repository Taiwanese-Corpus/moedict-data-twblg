from csv import DictReader
from os.path import basename, join

from django.core.management.base import BaseCommand
from django.utils import timezone


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 聽拍規範表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.基本物件.公用變數 import 分字符號
from 臺灣言語工具.基本物件.公用變數 import 分詞符號
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from django.core.management import call_command
from os import walk


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--匯入幾筆',
            type=int,
            default=100000,
            help='試驗用，免一擺全匯'
        )
        parser.add_argument(
            '音檔資料夾路徑',
            type=str,
        )

    def handle(self, *args, **參數):
        call_command('顯示資料數量')

        'https://github.com/g0v/moedict-data-twblg/tree/master/uni'
        詞目 = {}
        with open('語音合成訓練範例-臺語教典/詞目總檔.csv') as 檔案:
            for 一筆 in DictReader(檔案):
                編號 = 一筆['主編碼'].strip()
                漢字 = 一筆['詞目'].strip()
                拼音 = 一筆['音讀'].strip().split('/')[0]
                try:
                    正規化臺羅 = (
                        拆文分析器
                        .建立句物件(文章粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 拼音))
                        .轉音(臺灣閩南語羅馬字拼音)
                        .看型(物件分字符號=分字符號, 物件分詞符號=分詞符號)
                    )
                    拆文分析器.對齊組物件(漢字, 正規化臺羅)
                    詞目[int(編號)] = (漢字, 正規化臺羅)
                except 解析錯誤:
                    pass
        規範 = 聽拍規範表.objects.get_or_create(規範名='臺羅', 範例='無', 說明='bo5')[0]
        公家內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
            '來源': 來源表.objects.get_or_create(名='臺灣閩南語常用詞辭典')[0].編號(),
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0].pk,
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '臺灣',
            '著作年': str(timezone.now().year),
            '屬性': {'語者': '陳秀蓉'}
        }
        匯入數量 = 0
        for 音檔目錄, _資料夾, 路徑陣列 in walk(參數['音檔資料夾路徑']):
            for 路徑 in sorted(路徑陣列):
                音檔路徑 = join(音檔目錄, 路徑)
                if 音檔路徑.endswith('.wav'):
                    try:
                        音檔編號 = int(basename(音檔路徑).split('.')[0])
                        (漢字, 拼音) = 詞目[音檔編號]
                    except:  # 有的詞條尾仔提掉矣，親像編號5
                        pass
                    else:
                        影音內容 = {'影音所在': 音檔路徑}
                        影音內容.update(公家內容)
                        影音 = 影音表.加資料(影音內容)
                        句物件 = (
                            拆文分析器.對齊句物件(漢字, 拼音)
                            .轉音(臺灣閩南語羅馬字拼音)
                        )

                        json資料 = [{
                            '內容': 句物件.看分詞(),
                            '語者': '無註明',
                            '開始時間': 0,
                            '結束時間': 影音.聲音檔().時間長度(),
                        }]
                        聽拍內容 = {'規範': 規範, '聽拍資料': json資料}
                        聽拍內容.update(公家內容)
                        影音.寫聽拍(聽拍內容)

                        匯入數量 += 1
                        if 匯入數量 == 參數['匯入幾筆']:
                            break

        call_command('顯示資料數量')
