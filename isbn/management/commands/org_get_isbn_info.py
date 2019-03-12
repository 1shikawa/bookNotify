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
        # print("Djangoカスタムコマンドのテストです。")
        logging.info('[正常]楽天書籍情報収集処理を開始します。')

        word_list = []
        queryset = SearchWord.objects.all().filter(flag=True)
        for item in queryset:
            word_list.append(item.word)

        # print(word_list)
        # ここから下を追加
        for word in word_list:
            # 検索ワードに登録されているワードの書籍情報を検索
            API = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
            APPLICATION_ID = "1070374734242724400"
            values = {
                "applicationId": APPLICATION_ID,
                "format": "json",  # 出力形式
                "title": word
            }
            # パラメータのエンコード処理
            params = urllib.parse.urlencode(values)
            # リクエスト用のURLを生成
            url = API + "?" + params
            # リクエストを投げる。
            req = requests.get(url)
            # json形式で取得
            data = json.loads(req.text)
            pprint.pprint(data)


            for i in range(len(data['Items'])):
                # isbnコードが新規の場合
                if not Book.objects.filter(isbn=data['Items'][i]['Item']['isbn']).exists():
                    # 年月日を日付型に変換
                    if "日" not in data['Items'][i]['Item']['salesDate']:
                        salesDate = data['Items'][i]['Item']['salesDate'] + "01日"
                        salesDate = salesDate.replace('年', '/').replace('月', '/').replace('日', '')
                        salesDate = datetime.strptime(salesDate, '%Y/%m/%d')
                    else:
                        salesDate = data['Items'][i]['Item']['salesDate'].replace('年', '/').replace('月', '/').replace(
                            '日', '')
                        salesDate = datetime.strptime(salesDate, '%Y/%m/%d')

                    # 新規登録
                    isbn_data = Book.objects.create(
                        word=SearchWord.objects.get(word=word),
                        isbn=data['Items'][i]['Item']['isbn'],
                        salesDate=salesDate,
                        title=data['Items'][i]['Item']['title'],
                        itemPrice=data['Items'][i]['Item']['itemPrice'],
                        imageUrl=data['Items'][i]['Item']['mediumImageUrl'],
                        reviewAvg=data['Items'][i]['Item']['reviewAverage'],
                        reviewCnt=data['Items'][i]['Item']['reviewCount'],
                        itemUrl=data['Items'][i]['Item']['itemUrl'],
                    )

                    # 新刊をラインに通知
                    message = data['Items'][i]['Item']['itemUrl']
                    line_notify_token = 'GnXdOqWTkRCw85oHjB8nQGqkO388zjBx5AGBKWwKi0R'
                    line_notify_api = 'https://notify-api.line.me/api/notify'
                    payload = {'message': message}
                    headers = {'Authorization': 'Bearer ' + line_notify_token}
                    requests.post(line_notify_api, data=payload, headers=headers)

                # isbnコードが既存の場合
                else:
                    isbn_data = Book.objects.get(isbn=data['Items'][i]['Item']['isbn'])
                    # レビュー平均値の差異チェック
                    if data['Items'][i]['Item']['reviewAverage'] != isbn_data.reviewAvg:
                        isbn_data.reviewAvg = data['Items'][i]['Item']['reviewAverage']
                    # レビュー数の差異チェック
                    if data['Items'][i]['Item']['reviewCount'] != isbn_data.reviewCnt:
                        isbn_data.reviewCnt = data['Items'][i]['Item']['reviewCount']
                    isbn_data.save()

            logging.info('[正常]楽天書籍情報収集処理が正常終了しました。')