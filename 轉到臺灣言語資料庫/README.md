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
在`臺灣言語資料庫`專案目錄下
```bash
git clone https://github.com/Taiwanese-Corpus/moedict-data-twblg.git
sudo apt-get install -y python-virtualenv g++ libxml2-dev libxslt-dev python-dev
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
pip install -r moedict-data-twblg/轉到臺灣言語資料庫/requirements.txt
echo "from 轉到臺灣言語資料庫.整合到資料庫 import 走 ; 走()" | PYTHONPATH=moedict-data-twblg python manage.py shell
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