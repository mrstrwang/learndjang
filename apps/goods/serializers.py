from rest_framework import serializers
from django.db.models import Q

from .models import Goods, GoodsCategory,GoodsImage, Banner, GoodsCategoryBrand, IndexAd


class GoodsImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = GoodsImage
		fields = ('image',)


class CategorySerializer3(serializers.ModelSerializer):
	class Meta:
		model = GoodsCategory
		fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
	sub_cat = CategorySerializer3(many=True)

	class Meta:
		model = GoodsCategory
		fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
	# 关系字段外键自关联
	sub_cat = CategorySerializer2(many=True)

	class Meta:
		model = GoodsCategory
		fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
	category = CategorySerializer()
	images = GoodsImageSerializer(many=True)

	class Meta:
		# 一定要配置？？
		model = Goods
		fields = '__all__'
		# fields = ('category','name')


class BannerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Banner
		fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
	"""品牌序列化器"""

	class Meta:
		model = GoodsCategoryBrand
		fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
	"""首页商品序列化器"""
	brands = BrandSerializer(many=True)
	# goods的一对多
	goods = serializers.SerializerMethodField()
	# 对应的是商品类型的类目的耳机目录
	sub_cat = CategorySerializer3(many=True)

	def get_goods(self,obj):
		# 得到实实在在的商品数据
		all_goods = Goods.objects.filter(Q(category_id=obj.id)|
										 Q(category__parent_category_id=obj.id)|
										 Q(category__parent_category__parent_category_id=obj.id))
		goods_serializer = GoodsSerializer(all_goods,many=True, context={'request': self.context['request']})
		return goods_serializer.data

	ad_goods = serializers.SerializerMethodField()

	def get_ad_goods(self,obj):
		goods_json = {}
		ad_goods = IndexAd.objects.filter(category_id=obj.id)
		if ad_goods:
			goods_ins = ad_goods[0].goods
			goods_serializer = GoodsSerializer(goods_ins, many=False,context={"request":self.context["request"]})
			goods_json = goods_serializer.data

		return goods_json

	class Meta:
		model = GoodsCategory
		fields = '__all__'