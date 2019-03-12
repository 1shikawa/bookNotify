from django.contrib import admin
from .models import SearchWord, Book
# Register your models here.
class SearchWordAdmin(admin.ModelAdmin):
    list_display = ('pk', 'word')

class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'word', 'isbn', 'salesDate', 'title', 'itemPrice', 'imageUrl', 'reviewAvg', 'reviewCnt')

admin.site.register(SearchWord, SearchWordAdmin)
admin.site.register(Book, BookAdmin)