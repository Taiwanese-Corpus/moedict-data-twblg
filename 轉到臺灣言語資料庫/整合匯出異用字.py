# -*- coding: utf-8 -*-
from csv import DictReader
import json
from os import makedirs
from os.path import join, abspath, dirname

import yaml


from 轉到臺灣言語資料庫.整合到資料庫 import 整合到資料庫


class 整合匯出異用字():

    def 處理詞條(self):
        對應表 = self._詞目總檔編號漢字對應()
        全部下層 = []
        with open(join(dirname(abspath(__file__)), '..', 'x-異用字.json')) as 檔:
            for 主編碼, 異用字陣列 in sorted(json.load(檔).items()):
                for 異用字 in 異用字陣列:
                    全部下層.append({'相關資料組': [{'文本資料': 異用字}, {'文本資料': 對應表[主編碼]}]})
        全部資料 = {'種類': '字詞'}
        全部資料.update(整合到資料庫.公家內容)
        全部資料['來源'] = 整合到資料庫.教育部閩南語辭典
        全部資料['下層'] = 全部下層
        return 全部資料

    def _詞目總檔編號漢字對應(self):
        對應表 = {}
        with open(join(dirname(abspath(__file__)), '..', 'uni', '詞目總檔.csv')) as 檔:
            讀檔 = DictReader(檔)
            for row in 讀檔:
                對應表[row['主編碼']] = row['詞目']
        return 對應表

if __name__ == '__main__':
    makedirs(join(dirname(abspath(__file__)), '資料'), exist_ok=True)
    全部資料 = 整合匯出異用字().處理詞條()
    with open(join(dirname(abspath(__file__)), '資料', '異用字.yaml'), 'w') as 檔案:
        yaml.dump(全部資料, 檔案, default_flow_style=False, allow_unicode=True)
