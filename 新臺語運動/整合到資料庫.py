# -*- coding: utf-8 -*-
from 新臺語運動.整理外來詞 import 整理外來詞
from 新臺語運動.整理詞目總檔 import 整理詞目總檔


def 走():
    #     來源表.objects.get_or_create(名='系統管理')
    #     版權表.objects.get_or_create(版權='姓名標示-禁止改作 3.0 台灣')
    #     種類表.objects.get_or_create(種類=字詞)
    #     種類表.objects.get_or_create(種類=語句)

    公家內容 = {
        '收錄者': 1,
        '來源': 1,
        '版權': '會使公開',
        #         '種類':'字詞',
        '語言腔口': '閩南語',
        '著作所在地': '臺灣',
        '著作年': '2014',
        #         '屬性':self.詞屬性,
    }
    for 整合 in [整理詞目總檔(), 整理外來詞()]:
        for 詞條 in 整合.得著詞條():
            print(詞條)
