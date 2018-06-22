import os
import sys

#得到data目录

#得到当前文件的真实路径
real_path = os.path.realpath(__file__)


#转化成目录，等到当前文件所在的目录
file_path = os.path.dirname(real_path)


#把当前路径添加到运行环境中
sys.path.insert(0,file_path)
print(sys.path)

#设置model运行的独立环境
#这是在manage.py文件里面的路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Shop.settings")

import django
django.setup()

from goods.models import GoodsCategory
from db_tools.data.category_data import row_data
# all_GoodsCategory = GoodsCategory.objects.all()

#把数据存入数据库中
for level1_data in row_data:
	level1_instance = GoodsCategory()
	level1_instance.name = level1_data['name']
	level1_instance.code = level1_data['code']
	level1_instance.category_type = 1
	level1_instance.save()

	for level2_data in level1_data['sub_categorys']:
		level2_instance = GoodsCategory()
		level2_instance.name = level2_data['name']
		level2_instance.code = level2_data['code']
		level2_instance.category_type = 2
		level2_instance.parent_category = level1_instance
		level2_instance.save()

		for level3_data in level2_data['sub_categorys']:
			level3_instance = GoodsCategory()
			level3_instance.name = level3_data['name']
			level3_instance.code = level3_data['code']
			level3_instance.category_type = 3
			level3_instance.parent_category = level2_instance
			level3_instance.save()