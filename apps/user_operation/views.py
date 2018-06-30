from django.shortcuts import render
from rest_framework import viewsets,mixins,permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from user_operation.serializers import UserFavSerializers,UserFavDetailSerializers

from .serializers import LeavingMessageSerializers,UserAddressSerializers
from .models import UserFav,UserLeavingMessage,UserAddress
from utils.permissions import IsOwnerOrReadOnly
# Create your views here.


class UserAddressViewSet(viewsets.ModelViewSet):
	queryset = UserAddress.objects.all()
	serializer_class = UserAddressSerializers
	permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

	def get_queryset(self):
		# 返回当前登录用户的信息
		return UserAddress.objects.filter(user=self.request.user)


class LeavingMessageViewSet(mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
	"""用户留言"""
	queryset = UserLeavingMessage.objects.all()
	serializer_class = LeavingMessageSerializers
	permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

	def get_queryset(self):
		queryset = UserLeavingMessage.objects.all()
		# 返回当前登录用户的信息
		return queryset.filter(user=self.request.user)


class UserFavsViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
	"""用户收藏"""
	queryset = UserFav.objects.all()
	# 序列化
	# serializer_class = UserFavSerializers
	# 判断是否登陆，是不是同一个用户
	permissions_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
	# jwt认证，和SessionAuthentication登陆
	authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
	# 将第三个收藏表id变成商品id
	lookup_field = 'goods_id'

	def get_serializer_class(self):
		# 注册用户
		if self.action == 'create':
			return UserFavSerializers
		elif self.action == 'list':
			return UserFavDetailSerializers
		return UserFavDetailSerializers

	def get_queryset(self):
		return UserFav.objects.filter(user=self.request.user)