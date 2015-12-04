# 臺灣閩南語常用詞辭典-轉到臺灣言語資料庫

## 流程

### 資料
* `詞目總檔`、`又音`
  * `對應華語`、`異用字`
* `詞彙方言差`
* `例句`
* `外來詞`

### 對應關係
* `對應華語`→`閩南語資料`


## 匯入資料庫
```bash
python manage.py 匯入資料 https://Taiwanese-Corpus.github.io/moedict-data-twblg/轉到臺灣言語資料庫/資料/xls整理.yaml https://Taiwanese-Corpus.github.io/moedict-data-twblg/轉到臺灣言語資料庫/資料/異用字.yaml
```

## 開發試驗
###環境
在`moedict-data-twblg`專案目錄下
```
sudo apt-get install -y python-virtualenv g++ libxml2-dev libxslt-dev python3-dev libz-dev
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r 轉到臺灣言語資料庫/requirements.txt
```

### 試驗
```
python -m unittest
```

### 產生yaml檔
```
PYTHONPATH=. python 轉到臺灣言語資料庫/整合到資料庫.py
PYTHONPATH=. python 轉到臺灣言語資料庫/整合匯出異用字.py

```