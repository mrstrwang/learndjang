from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import viewsets

from .models import Goods
from .serializers import GoodsSerializer

# from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter

# Create your views here.


class GoodsListPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	page_query_param = 'page'


class GoodsListView(mixins.ListModelMixin,viewsets.GenericViewSet):
	"""商品详情"""
	# 终极版
	# 得到所有的商品
	queryset = Goods.objects.all()
	#序列化期
	serializer_class = GoodsSerializer
	#添加分页配置，setting.py就可以省略了
	pagination_class = GoodsListPagination

	# 自定义过滤器
	filter_class = GoodsFilter


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

