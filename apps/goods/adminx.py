from .models import GoodsCategory,Goods,GoodsCategoryBrand,GoodsImage
import xadmin
from xadmin import views


class GoodsAdmin(object):
	list_display = ["name","click_num","sold_num","fav_num","is_hot","shop_price","goods_nums"]
	#对商品详细描述，设置富文本这样样式
	style_fields = {"goods_desc": "ueditor"}
	#对商品某些字段提供搜索
	search_fields = ["name","goods_desc","goods_brief"]


	class GoodsImageLine(object):
		model = GoodsImage
		exclude = ["add_time"]
		#每次添加一张
		extra = 1
		#显示风格，以表格的方式薪水
		style = "tab"

	inlines = [GoodsImageLine]


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