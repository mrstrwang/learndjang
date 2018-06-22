from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField

# Create your models here.

class GoodsCategory(models.Model):
	"""商品类型"""
	CATEGORY_TYPE = (
		(1,"一级类目"),
		(2, "二级类目"),
		(3, "三级类目"),

	)
	#类目名称
	name = models.CharField(max_length=30,verbose_name="类目名称")

	#类目code
	code = models.CharField(max_length=30,verbose_name="类目code")

	#类目描述
	desc = models.TextField(max_length=100,verbose_name="类目描述")

	#当前类目级别
	category_type = models.CharField(max_length=30,verbose_name="当前类别",choices=CATEGORY_TYPE)

	#父级类目related_name="sub_cat"关联的表联系起来
	parent_category = models.ForeignKey("self",verbose_name="父级类目",null=True,blank=True,related_name="sub_cat")

	#是否导航
	is_tab = models.BooleanField(default=False,verbose_name="是否导航")

	#添加时间
	add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

	#在后台管理的时候中文呈现
	class Meta:
		verbose_name = "商品类型"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


class GoodsCategoryBrand(models.Model):
	"""商品品牌"""


	#商品类型
	category = models.ForeignKey(GoodsCategory,verbose_name="商品类型",blank=True,null=True,related_name="brands")
	#名称
	name = models.CharField(max_length=100,verbose_name="品牌名称")
	#图片
	image= models.ImageField(max_length=200,verbose_name="品牌图片",upload_to="goods/images/")
	#品牌描述
	desc = models.CharField(max_length=1000,verbose_name="品牌描述")
	#添加时间
	add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

	#在后台管理的时候中文呈现
	class Meta:
		verbose_name = "商品品牌"
		verbose_name_plural = verbose_name
		db_table = "goods_goodsbrand"

	def __str__(self):
		return self.name


#商品
class Goods(models.Model):
	#类目
	category = models.ForeignKey(GoodsCategory,verbose_name="类目",related_name="category",null=True,blank=True)
	#商品编号唯一描述
	goods_sn = models.CharField(max_length=50,verbose_name="商品编号")
	#商品名称
	name = models.CharField(max_length=50,verbose_name="商品名称")
	#商品简单描述
	goods_brief = models.CharField(max_length=200,verbose_name="商品简介")
	#点击量
	click_num = models.IntegerField(default=0,verbose_name="点击量")
	#销售量
	sold_num = models.IntegerField(default=0,verbose_name="销量")
	#收藏数
	fav_num = models.IntegerField(default=0,verbose_name="收藏数")
	#富文本商品介绍
	goods_desc = UEditorField(default="",width=1000,height=300,verbose_name="富文本商品介绍",imagePath="goods/images/",filePath="goods/files/")

	goods_nums = models.IntegerField(default=0,verbose_name='商品库存')
	#商品封面
	goods_front_image = models.ImageField(upload_to="goods/images/",verbose_name="图片封面",null=True,blank=True)
	#是否包邮
	ship_free = models.BooleanField(default=True,verbose_name="是否包邮")
	#市场价格
	market_price = models.FloatField(default=0.0,verbose_name="市场价格")
	#本店价格
	shop_price = models.FloatField(default=0.0,verbose_name="本店价格")
	#是否新品
	is_new = models.BooleanField(default=False,verbose_name="是否新品")
	#是否热卖
	is_hot = models.BooleanField(default=False,verbose_name="是否热卖")
	# 添加时间
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	# 在后台管理的时候中文呈现
	class Meta:
		verbose_name = "商品"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


#商品的轮播图
class GoodsImage(models.Model):

	#商品
	goods = models.ForeignKey(Goods,verbose_name="商品",related_name="images")
	#图片
	image = models.ImageField(max_length=200,upload_to="goods/images/",verbose_name="商品轮播图的一张",default="")
	# 添加时间
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	# 在后台管理的时候中文呈现
	class Meta:
		verbose_name = "商品的轮播图"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.goods.name

class Banner(models.Model):
	"""首页轮播图"""
	#商品
	goods = models.ForeignKey(Goods,verbose_name="商品")
	#图片
	image = models.ImageField(upload_to="banner",max_length=200,verbose_name="图片")
	#播放顺序
	index = models.IntegerField(default=0,verbose_name="播放顺序")
	#添加时间
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	# 在后台管理的时候中文呈现
	class Meta:
		verbose_name = "首页轮播图"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.goods.name
