from rest_framework import serializers
from .models import Goods,GoodsCategory,GoodsImage


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
	#关系字段外键自关联
	sub_cat = CategorySerializer2(many=True)

	class Meta:
		model = GoodsCategory
		fields = '__all__'

class GoodsSerializer(serializers.ModelSerializer):
	category = CategorySerializer()
	images = GoodsImageSerializer(many=True)
	class Meta:
		#一定要配置？？
		model = Goods
		fields = '__all__'
		# fields = ('category','name')


