import os
import sys

# 得到当前文件的位置和名称
filename_path = os.path.realpath(__file__)

dirname = os.path.dirname(filename_path)

sys.path.insert(0,dirname)


# 设置独立使用models--从manage.py拷贝过来的
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Shop.settings")


#导入django的设置
import django
django.setup()

# 这行代码不能卸载前面，一定要写在django.setup()的后面
from goods.models import Goods,GoodsImage,GoodsCategoryBrand,GoodsCategory
# 导入数据
from db_tools.data.product_data import row_data
# i = 1
for goods_detail in row_data:
	# print(goods_detail)
	goods = Goods()
	goods.name = goods_detail["name"]
	goods.market_price = float(goods_detail["market_price"].replace("￥","").replace("元",""))
	goods.shop_price = float(goods_detail["sale_price"].replace("￥","").replace("元",""))
	# 商品简单描述
	# 下面语法的含义是：如果goods_detail["desc"]不为None直接返回，否则返回”“
	goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
	# 商品富文本描述
	goods.goods_desc =  goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
	# 商品封面取images的第一张图片
	# 如果没有就返回”“
	goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] is not None else ""
	categorys_name =goods_detail["categorys"][-1]
	categorys = GoodsCategory.objects.filter(name=categorys_name)
	if categorys:
		goods.category = categorys[0]

	goods.save()


	for goods_image in goods_detail["images"]:
		goods_image_instace = GoodsImage()
		goods_image_instace.image = goods_image
		goods_image_instace.goods = goods
		goods_image_instace.save()

