from django.db import models
from django.utils import timezone

# Create your models here.
# 検索ワードモデル
class SearchWord(models.Model):
    class Meta:
        verbose_name = '検索ワード'
        verbose_name_plural = '検索ワード'

    word = models.CharField(max_length=255)
    flag = models.BooleanField(verbose_name='有効フラグ',default=False)

    def __str__(self):
        return self.word

# 書籍情報モデル
class Book(models.Model):
    class Meta:
        verbose_name = '書籍情報'
        verbose_name_plural = '書籍情報'

    word = models.ForeignKey(SearchWord, on_delete=models.PROTECT, verbose_name='検索ワード')
    isbn = models.BigIntegerField('書籍コード', unique=True)
    salesDate = models.DateField('発売日', default=timezone.now, blank=True, null=True)
    title = models.CharField('書籍タイトル', max_length=255)
    itemPrice = models.IntegerField('税込み価格', default=1, help_text='単位は円',blank=True, null=True )
    imageUrl = models.URLField('画像URL', blank=True, null=True)
    reviewAvg = models.FloatField('レビュー平均点', default=0, blank=True, null=True)
    reviewCnt = models.IntegerField('レビュー件数', default=1, blank=True, null=True)
    itemUrl = models.URLField('商品URL',blank=True, null=True)

    def __str__(self):
        return self.title