# -*- coding: utf-8 -*-

from html.parser import HTMLParser
import urllib.request


from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡


class 整理外來詞:

    class 網頁剖析工具(HTMLParser):
        剖析結果 = []
        目前這逝 = []
        目前這格 = ''
        愛記錄 = False

        def 目前剖析結果(self):
            return self.剖析結果

        def handle_starttag(self, tag, attrs):
            if tag == "table" and ('class', 'fuluTab') in attrs:
                self.愛記錄 = True
            if self.愛記錄:
                if tag == "tr":
                    self.目前這逝 = []
                elif tag == "td":
                    self.目前這格 = ''

        def handle_endtag(self, tag):
            if tag == "table":
                self.愛記錄 = False
            if self.愛記錄:
                if tag == "tr":
                    self.剖析結果.append(self.目前這逝)
                elif tag == "td":
                    self.目前這逝.append(self.目前這格)

        def handle_data(self, data):
            if self.愛記錄:
                self.目前這格 += data.strip()

    def __init__(self):
        self.粗胚 = 文章粗胚()
        self.分析器 = 拆文分析器()
        self.譀鏡 = 物件譀鏡()

    def 得著詞條(self):
        網址 = 'http://twblg.dict.edu.tw/holodict_new/index/fulu_wailaici.jsp'
        資料 = urllib.request.urlopen(網址).read().decode("utf8")
        網頁工具 = self.網頁剖析工具()
        網頁工具.feed(資料)
        結果 = 網頁工具.剖析結果
        for 一筆 in 結果[1:]:
            原本音標 = 一筆[1].replace(' ', '-')
            標準音標 = self.音標處理(原本音標)
            華語 = 一筆[2].strip().split('、')
#             print(原本音標,標準音標)
            try:
                for 日語文本 in 一筆[3:6]:
                    yield {
                        '文本資料': 日語文本,
                        '種類': 字詞,
                        '華語': 華語,
                        '校對': [(標準音標, '')]
                    }
            except Exception as 問題:
                #                 對照表格式 = "'{0}':'{0}', #{1}，{2}"
                #                 print(對照表格式.format(原本假名,標準音標,一筆[2]))
                print(問題)

    def 音標處理(self, 原本音標):
        #                 詞物件 = 分析器.建立詞物件(標準音標)
        音 = self.粗胚 .數字英文中央全加分字符號(原本音標)
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
        return 音
