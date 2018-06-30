from django_filters import rest_framework as filters
from .models import Goods
from django.db.models import Q


class GoodsFilter(filters.FilterSet):
	pricemin = filters.NumberFilter(name='shop_price',lookup_expr='gte')
	pricemax = filters.NumberFilter(name='shop_price',lookup_expr='lte')
	name = filters.CharFilter(name='name',lookup_expr='icontains')
	# 支持前端新的字段过滤
	top_category = filters.NumberFilter(method='top_category_filters')

	def top_category_filters(self,queryset,name,value):
		queryset = queryset.filter(Q(category__id=value)|Q(category__parent_category_id=value))

		return queryset

	class Meta:
		model = Goods
		fields = ['pricemin', 'pricemax', 'name', 'is_hot', 'is_new']