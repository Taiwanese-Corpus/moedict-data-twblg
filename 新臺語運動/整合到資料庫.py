# -*- coding: utf-8 -*-
from 新臺語運動.整理外來詞 import 整理外來詞
from 新臺語運動.整理詞目總檔 import 整理詞目總檔
from 新臺語運動.整理又音 import 整理又音
from 新臺語運動.整理方言詞 import 整理方言詞
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 文本表


class 整合到資料庫:
    教育部閩南語辭典 = 來源表.objects.get_or_create(名='教育部閩南語辭典')[0].編號()
    薛丞宏 = 來源表.objects.get_or_create(名='薛丞宏')[0].編號()
    版權 = 版權表.objects.get_or_create(版權='姓名標示-禁止改作 3.0 台灣')[0].pk
    公家內容 = {
        '版權': 版權,
        #         '種類':'字詞',
        '語言腔口': '閩南語',
        '著作所在地': '臺灣',
        '著作年': '2015',
    }

    def 處理詞條(self, 詞條, 收錄者):
        公家內容 = {
            '收錄者': 收錄者,
        }
        公家內容.update(self.公家內容)
        try:
            for 華語 in 詞條['華語']:
                華語內容 = {
                    '來源': self.教育部閩南語辭典,
                    '種類': 詞條['種類'],
                    '外語語言': '華語',
                    '外語資料': 華語,
                }
                華語內容.update(公家內容)
                外語 = 外語表.加資料(華語內容)
                self.加臺語詞條(公家內容, 詞條, 外語)
        except KeyError:
            self.加臺語詞條(公家內容, 詞條, None)

    def 加臺語詞條(self, 公家內容, 詞條, 外語):
        臺語內容 = {
            '來源': self.教育部閩南語辭典,
            '種類': 詞條['種類'],
            '文本資料': 詞條['文本資料'],
        }
        try:
            臺語內容['屬性'] = 詞條['屬性']
        except:
            pass
        臺語內容.update(公家內容)
        if 外語:
            文本 = 外語.翻母語(臺語內容)
        else:
            文本 = 文本表.加資料(臺語內容)
        try:
            for 漢字, 音標 in 詞條['校對']:
                校對內容 = {
                    '來源': self.薛丞宏,
                    '種類': 詞條['種類'],
                    '文本資料': 漢字,
                }
                if 音標:
                    校對內容['屬性'] = {'音標': 音標}
                校對內容.update(公家內容)
                文本.校對做(校對內容)
        except KeyError:
            pass


def 走(收錄者=整合到資料庫.薛丞宏):

    到資料庫 = 整合到資料庫()
    for 整合 in [
        整理詞目總檔(),
        整理又音(),
        整理方言詞(),
        整理外來詞(),
    ]:
        for _第幾个, 詞條 in enumerate(整合.得著詞條()):
            try:
                到資料庫.處理詞條(詞條, 收錄者)
            except Exception as e:
                print(詞條,e)
                raise
