# from django.shortcuts import render
# from django.views.generic import View
#  from .models import Goods
# from django.http.response import JsonResponse,HttpResponse
# from django.core.serializers import serialize
# import json

# from .models import Goods
# from .serializers import GoodsSerializer
# from rest_framework.response import Response
# from rest_framework.views import APIView

from .models import Goods
from rest_framework import mixins
from rest_framework import generics
from .serializers import GoodsSerializer

# Create your views here.

class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
	"""商品详情"""
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer

	def get(self,request):
		return self.list(request)


	# def get(self,request,format=None):
	# 	goods = Goods.objects.all()[:10]
	# 	goods_serializer = GoodsSerializer(goods, many=True)
	# 	return Response(data=goods_serializer.data)

	# def get(self,request):
	# 	goods_list = Goods.objects.all()[:10]
	# 	data = serializers.serialize('json',goods_list)
	# 	return HttpResponse(data,'application/json')

	# def get(self,request):
	# 	goods_list = Goods.objects.all()[:10]
	# 	data = serialize('json',goods_list)
	# 	data = json.loads(data)
	# 	return JsonResponse(data,safe=False)

