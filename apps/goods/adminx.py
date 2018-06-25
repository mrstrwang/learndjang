from .models import GoodsCategory,Goods,GoodsCategoryBrand,GoodsImage
import xadmin


class GoodsAdmin(object):
	list_display = ['name','click_num','sold_num',"fav_num","market_price",
					"shop_price","goods_desc","is_new","is_hot","add_time"]
	search_fields = ['name']


class GoodsCategoryAdmin(object):
	list_display = ['name', 'category_type', 'is_tab']
	list_filter = ['category_type']


class GoodsCategoryBrandAdmin(object):
	pass


class GoodsImageAdmin(object):
	pass


xadmin.site.register(Goods,GoodsAdmin)
xadmin.site.register(GoodsCategory,GoodsCategoryAdmin)
xadmin.site.register(GoodsCategoryBrand,GoodsCategoryBrandAdmin)
xadmin.site.register(GoodsImage,GoodsImageAdmin)