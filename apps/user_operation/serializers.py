from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav,UserLeavingMessage,UserAddress
from goods.serializers import GoodsSerializer


class UserAddressSerializers(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M')

	class Meta:
		model = UserAddress
		fields = '__all__'


class UserFavSerializers(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = UserFav
		validators = [
			UniqueTogetherValidator(
				queryset=UserFav.objects.all(),
				fields=('goods','user'),
				message='已经收藏le'
			)
		]
		fields = ('user','goods','id')


class UserFavDetailSerializers(serializers.ModelSerializer):
	goods = GoodsSerializer()

	class Meta:
		model = UserFav
		fields = ('goods','id')


class LeavingMessageSerializers(serializers.ModelSerializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M')

	class Meta:
		model = UserLeavingMessage
		fields = ("user","subject","msg_type","message","file","add_time","id")
