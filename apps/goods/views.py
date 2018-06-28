from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins,viewsets,filters
from rest_framework.authentication import TokenAuthentication

from .models import Goods,GoodsCategory
from .serializers import GoodsSerializer,CategorySerializer

from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
# 代码实现自定义用户验证


class GoodsListPagination(PageNumberPagination):
	page_size = 8
	page_size_query_param = 'page_size'
	page_query_param = 'page'


class GoodsViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
	"""商品详情"""
	# 终极版
	# 得到所有的商品
	queryset = Goods.objects.all()
	# 序列化器
	serializer_class = GoodsSerializer
	#添加分页配置，setting.py就可以省略了
	pagination_class = GoodsListPagination
	# 自定义过滤器
	filter_class = GoodsFilter
	#支持搜索和过滤，写在一起
	filter_backends = (filters.OrderingFilter,DjangoFilterBackend,filters.SearchFilter)
	search_fields = ('name', 'goods_desc', 'goods_brief')
	ordering_fields = ('shop_price', 'add_time')
	authentication_classes = (TokenAuthentication,)

	def get_queryset(self):
		# 得到所有商品
		queryset = Goods.objects.all()
		# 得到最低价格
		pricemin = self.request.query_params.get("pricemin", 0)	 # 10
		if pricemin:
			queryset = queryset.filter(shop_price__gte=int(pricemin))
		return queryset

	# get请求
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


# 商品类型接口
class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	queryset = GoodsCategory.objects.filter(category_type=1)
	# 指定序列化器
	serializer_class = CategorySerializer

