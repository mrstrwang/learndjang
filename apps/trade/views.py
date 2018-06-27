from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ShopingCart
from .serializers import ShopingCartSerializer,ShopingCartDetailSeralizer
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.
class ShopingCartViewSet(viewsets.ModelViewSet):
	queryset = ShopingCart.objects.all()
	# 序列化器被get_serializer_class重写
	# serializer_class = ShopingCartSerializer
	permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
	# JWT认证
	authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
	lookup_field = 'goods_id'

	def get_serializer_class(self):
		if self.action == 'list':
			return ShopingCartDetailSeralizer
		else:
			return ShopingCartSerializer

	def get_queryset(self):
		return ShopingCart.objects.filter(user=self.request.user)