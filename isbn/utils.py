from isbn.models import Book, SearchWord
import urllib.parse
import requests
from datetime import datetime


def get_word_list():
    # 検索ワードリストの生成
    word_list = []
    queryset = SearchWord.objects.all().filter(flag=True)
    for item in queryset:
        word_list.append(item.word)
    return word_list


def create_url(word):
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
    return url


def lineNotify(message):
    line_notify_token = 'GnXdOqWTkRCw85oHjB8nQGqkO388zjBx5AGBKWwKi0R'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)


def regist_data(data, word):
    for i in range(len(data['Items'])):
        if not Book.objects.filter(isbn=data['Items'][i]['Item']['isbn']).exists():
            # 年月日を日付型に変換
            if "日" not in data['Items'][i]['Item']['salesDate']:
                salesDate = data['Items'][i]['Item']['salesDate'] + "01日"
                salesDate = salesDate.replace('年', '/').replace('月', '/').replace('日', '')
                salesDate = datetime.strptime(salesDate, '%Y/%m/%d')
            else:
                salesDate = data['Items'][i]['Item']['salesDate'].replace('年', '/').replace('月', '/').replace('日', '')
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
            lineNotify(message)
        # 既存エントリーの場合（レビュー数、レビュー平均値の差分だけを更新）
        else:
            # 現在のBookレコードを取得
            isbn_data = Book.objects.get(isbn=data['Items'][i]['Item']['isbn'])
            # 差分があれば更新
            if data['Items'][i]['Item']['reviewAverage'] != isbn_data.reviewAvg:
                isbn_data.reviewAvg = data['Items'][i]['Item']['reviewAverage']
            if data['Items'][i]['Item']['reviewCount'] != isbn_data.reviewCnt:
                isbn_data.reviewCnt = data['Items'][i]['Item']['reviewCount']

            # 反映
            isbn_data.save()