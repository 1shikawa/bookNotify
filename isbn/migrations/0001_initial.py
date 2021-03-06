# Generated by Django 2.1.7 on 2019-03-12 04:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.BigIntegerField(unique=True, verbose_name='書籍コード')),
                ('salesDate', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='発売日')),
                ('title', models.CharField(max_length=255, verbose_name='書籍タイトル')),
                ('itemPrice', models.IntegerField(blank=True, default=1, help_text='単位は円', null=True, verbose_name='税込み価格')),
                ('imageUrl', models.URLField(blank=True, null=True, verbose_name='画像URL')),
                ('reviewAvg', models.FloatField(blank=True, default=0, null=True, verbose_name='レビュー平均点')),
                ('reviewCnt', models.IntegerField(blank=True, default=1, null=True, verbose_name='レビュー件数')),
                ('itemUrl', models.URLField(blank=True, null=True, verbose_name='商品URL')),
            ],
            options={
                'verbose_name': '書籍情報',
                'verbose_name_plural': '書籍情報',
            },
        ),
        migrations.CreateModel(
            name='SearchWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
                ('flag', models.BooleanField(default=False, verbose_name='有効フラグ')),
            ],
            options={
                'verbose_name': '検索ワード',
                'verbose_name_plural': '検索ワード',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='isbn.SearchWord', verbose_name='検索ワード'),
        ),
    ]
