from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav


class UserFavSerializers(serializers.ModelSerializer):
	'''用户收藏序列器'''
	# 得到当前用户
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