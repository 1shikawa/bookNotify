from isbn.utils import get_word_list, create_url, lineNotify, regist_data
from django.core.management.base import BaseCommand
from isbn.models import Book, SearchWord
from datetime import datetime
import requests
import urllib.request
import urllib.parse
import json
import logging
import pprint

#初期パラメータ設定
logdir = r"C:\Users\toru-ishikawa\PycharmProjects\bookNotify\bookNotify\log"
#現在時刻の取得
date_name = datetime.now().strftime("%Y%m%d-%H%M%S")
#ファイル名の生成
file_name = logdir + "\\" + date_name +  "_" + "GET_ISBN_INFO.log"
logging.basicConfig(filename=file_name,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Command(BaseCommand):
    """ カスタムコマンド定義 """

    def handle(self, *args, **options):
        # ここに実行したい処理を書く
        logging.info('[正常]楽天書籍情報収集処理を開始します。')
        # 検索ワードの取得
        word_list = get_word_list()
        # 検索ワードを1つずつ取りだしてループ処理
        for word in word_list:
            # urlを生成
            url = create_url(word)
            # ダウンロード
            req = requests.get(url)
            # json形式で取得
            data = json.loads(req.text)
            # データの登録 or 変更(新規ならLineへ通知）
            regist_data(data, word)
        logging.info('[正常]楽天書籍情報収集処理が正常終了しました。')
