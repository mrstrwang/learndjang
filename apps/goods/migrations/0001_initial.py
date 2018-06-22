# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-21 01:38
from __future__ import unicode_literals

import DjangoUeditor.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=200, upload_to='banner', verbose_name='图片')),
                ('index', models.IntegerField(default=0, verbose_name='播放顺序')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name_plural': '首页轮播图',
                'verbose_name': '首页轮播图',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_sn', models.CharField(max_length=50, verbose_name='商品编号')),
                ('name', models.CharField(max_length=50, verbose_name='商品名称')),
                ('goods_brief', models.CharField(max_length=200, verbose_name='商品简介')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击量')),
                ('sold_num', models.IntegerField(default=0, verbose_name='销量')),
                ('fav_num', models.IntegerField(default=0, verbose_name='收藏数')),
                ('goods_desc', DjangoUeditor.models.UEditorField(default='', verbose_name='富文本商品介绍')),
                ('goods_front_image', models.ImageField(blank=True, null=True, upload_to='goods/images/', verbose_name='图片封面')),
                ('ship_free', models.BooleanField(default=True, verbose_name='是否包邮')),
                ('market_price', models.FloatField(default=0.0, verbose_name='市场价格')),
                ('shop_price', models.FloatField(default=0.0, verbose_name='本店价格')),
                ('is_new', models.BooleanField(default=False, verbose_name='是否新品')),
                ('is_hot', models.BooleanField(default=False, verbose_name='是否热卖')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name_plural': '商品',
                'verbose_name': '商品',
            },
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='类目名称')),
                ('code', models.CharField(max_length=30, verbose_name='类目code')),
                ('desc', models.TextField(max_length=100, verbose_name='类目描述')),
                ('category_type', models.CharField(choices=[(1, '一级类目'), (2, '二级类目'), (3, '三级类目')], max_length=30, verbose_name='当前类别')),
                ('is_tab', models.BooleanField(default=False, verbose_name='是否导航')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_cat', to='goods.GoodsCategory', verbose_name='父级类目')),
            ],
            options={
                'verbose_name_plural': '商品类型',
                'verbose_name': '商品类型',
            },
        ),
        migrations.CreateModel(
            name='GoodsCategoryBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='品牌名称')),
                ('image', models.ImageField(max_length=200, upload_to='goods/images/', verbose_name='品牌图片')),
                ('desc', models.CharField(max_length=1000, verbose_name='品牌描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='goods.GoodsCategory', verbose_name='商品类型')),
            ],
            options={
                'db_table': 'goods_goodsbrand',
                'verbose_name_plural': '商品品牌',
                'verbose_name': '商品品牌',
            },
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='', max_length=200, upload_to='goods/images/', verbose_name='商品轮播图的一张')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='goods.Goods', verbose_name='商品')),
            ],
            options={
                'verbose_name_plural': '商品的轮播图',
                'verbose_name': '商品的轮播图',
            },
        ),
        migrations.AddField(
            model_name='goods',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='goods.GoodsCategory', verbose_name='类目'),
        ),
        migrations.AddField(
            model_name='banner',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品'),
        ),
    ]
