from rest_framework import serializers

from .models import Goods,ShopingCart
from goods.serializers import GoodsSerializer


class ShopingCartSerializer(serializers.Serializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	nums = serializers.IntegerField(required=True,min_value=1,help_text='商品的数量')
	goods = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

	def update(self, instance, validated_data):
		nums = validated_data['nums']
		instance.nums = nums
		instance.save()
		return instance

	def create(self, validated_data):
		user = self.context['request'].user
		nums = validated_data['nums']
		goods = validated_data['goods']

		exised = ShopingCart.objects.filter(user=user,goods=goods)
		if exised:
			exised = exised[0]
			exised.nums += nums
			exised.save()
		else:
			exised = ShopingCart.objects.create(**validated_data)
		return exised


class ShopingCartDetailSeralizer(serializers.ModelSerializer):
	goods = GoodsSerializer(many=False)

	class Meta:
		model = ShopingCart
		fields = '__all__'
