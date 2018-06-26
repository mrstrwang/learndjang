from django.shortcuts import render
from rest_framework import viewsets,mixins,permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from user_operation.serializers import UserFavSerializers

from .models import UserFav
from utils.permissions import IsOwnerOrReadOnly
# Create your views here.

class UserFavsViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
	queryset = UserFav.objects.all()
	#序列化
	serializer_class = UserFavSerializers
	# 判断是否登陆，是不是同一个用户
	permissions_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
	# jwt认证，和SessionAuthentication登陆
	authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
	lookup_field = 'goods_id' #将第三个收藏表id变成商品id

	def get_queryset(self):
		return UserFav.objects.filter(user=self.request.user)
