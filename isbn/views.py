from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from isbn.models import Book, SearchWord
from .forms import SearchWordFrom
from django.urls import reverse_lazy
import subprocess

# Create your views here.
class BookListView(ListView):
    model = Book
    template_name = 'isbn/isbn_list.html'

    # 書籍情報テーブルの全データを取得するメソッドを定義
    def get_queryset(self):
        return Book.objects.all()

class SearchWordCreateView(CreateView):
    model = SearchWord
    form_class = SearchWordFrom
    # 登録処理が正常終了した場合の遷移先を指定
    success_url = reverse_lazy('isbn:create_done')

def create_done(request):
    # 登録処理が正常終了した場合に呼ばれるテンプレートを指定
    return render(request, 'isbn/create_done.html')

class WordListView(ListView):
    model = SearchWord
    template_name = 'isbn/searchword_list.html'

    def get_queryset(self):
        return SearchWord.objects.all()

class WordUpdateView(UpdateView):
    model = SearchWord
    form_class = SearchWordFrom
    success_url = reverse_lazy('isbn:update_done')

def update_done(request):
    return render(request, 'isbn/update_done.html')

class WordDeleteView(DeleteView):
    model = SearchWord
    success_url = reverse_lazy('isbn:delete_done')

def delete_done(request):
    return render(request, 'isbn/delete_done.html')

def update_isbn_info(request):
    message = []
    rc_code = None
    if request.POST:
        cmd = 'python manage.py get_isbn_info'
        rc_code = subprocess.call(cmd, shell=True)

        if rc_code == 0:
            message = '"楽天書籍情報の更新処理が正常終了しました。'
        else:
            message = '"楽天書籍情報の更新処理が異常終了しました。'

    return render(request, 'isbn/result.html', {'message':message})
