from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import viewsets

from .models import Goods,GoodsCategory
from .serializers import GoodsSerializer,CategorySerializer

# from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter

# Create your views here.


class GoodsListPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	page_query_param = 'page'


class GoodsViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
	"""商品详情"""
	# 终极版
	# 得到所有的商品
	queryset = Goods.objects.all()
	#序列化器
	serializer_class = GoodsSerializer
	#添加分页配置，setting.py就可以省略了
	pagination_class = GoodsListPagination
	# 自定义过滤器
	filter_class = GoodsFilter

#商品类型接口
class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	queryset = GoodsCategory.objects.filter(category_type=1)
	#指定序列化器
	serializer_class = CategorySerializer

