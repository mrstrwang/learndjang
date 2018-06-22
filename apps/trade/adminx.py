from .models import OrderGoods,ShopingCart,OrderInfo
import xadmin


class OrderGoodsAdmin(object):
	pass


class OrderInfoAdmin(object):
	pass


class ShopingCartAdmin(object):
	pass


xadmin.site.register(OrderGoods,OrderGoodsAdmin)
xadmin.site.register(OrderInfo,OrderInfoAdmin)
xadmin.site.register(ShopingCart,ShopingCartAdmin)
