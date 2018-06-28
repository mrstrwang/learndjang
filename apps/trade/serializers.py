from rest_framework import serializers

from .models import Goods,ShopingCart, OrderInfo ,OrderGoods
from goods.serializers import GoodsSerializer
from utils.alipay import AliPay
from Shop.settings import app_private_key_path, alipay_public_key_path


class ShopingCartSerializer(serializers.Serializer):
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	nums = serializers.IntegerField(required=True,min_value=1,help_text='商品的数量')
	goods = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

	def update(self, instance, validated_data):
		nums = validated_data['nums']
		instance.nums = nums
		instance.save()
		return instance

	def create(self, validated_data):
		user = self.context['request'].user
		nums = validated_data['nums']
		goods = validated_data['goods']

		exised = ShopingCart.objects.filter(user=user,goods=goods)
		if exised:
			exised = exised[0]
			exised.nums += nums
			exised.save()
		else:
			exised = ShopingCart.objects.create(**validated_data)
		return exised


class ShopingCartDetailSeralizer(serializers.ModelSerializer):
	goods = GoodsSerializer(many=False)

	class Meta:
		model = ShopingCart
		fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
	"""订单序列化器"""

	# 得到当前用户,在fields里面填写
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	# 订单号不让前端编写
	order_sn = serializers.CharField(read_only=True)
	# 交易号不让前端编写
	trade_sn = serializers.CharField(read_only=True)
	# 支付状态
	pay_status = serializers.CharField(read_only=True)
	# 支付时间
	pay_time = serializers.DateTimeField(read_only=True)
	# 添加时间
	add_time = serializers.DateTimeField(read_only=True)
	# 自定义生成订单号信息
	def generate_order_sn(self):
		import time
		from random import randint
		# "当前时间+userid+随机数"
		order_sn = "{time_str}{userid}{randstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),userid=self.context["request"].user, randstr=randint(10, 99))
		return order_sn

	def validate(self, attrs):
		# 添加订单
		attrs["order_sn"] = self.generate_order_sn()
		return attrs

	class Meta:
		model = OrderInfo
		fields = "__all__"


class OrderInfoSerializer(serializers.ModelSerializer):

	# 得到当前用户
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault()
	)

	order_sn = serializers.CharField(read_only=True)
	trade_no = serializers.CharField(read_only=True)
	pay_status = serializers.CharField(read_only=True)
	pay_time = serializers.DateTimeField(read_only=True)
	add_time = serializers.DateTimeField(read_only=True)

	alipay_url = serializers.SerializerMethodField(read_only=True)

	#obj就是model
	def get_alipay_url(self,obj):
		alipay = AliPay(
			appid="2016091300503105",

			# post请求
			app_notify_url="http://118.190.202.67:8000/alipay/return/",
			app_private_key_path=app_private_key_path,
			alipay_public_key_path=alipay_public_key_path,
			# 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
			debug=True,  # 默认False,
			# get请求
			return_url="http://118.190.202.67:8000/alipay/return/"
		)


		url = alipay.direct_pay(
			subject=obj.order_sn,
			out_trade_no= obj.order_sn,
			total_amount=obj.order_mount
		)
		# 沙箱环境
		re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
		# 点击后可以支付的连接
		# print(re_url)
		return re_url

	#生成订单号
	def get_order_sn(self):
		#怎么保证订单号唯一呢
		import time
		import random
		#当前时间+用户id+随机的两位数
		order_sn = "{curtime}{userid}{randint_str}".format(curtime=time.strftime("%Y%m%d%H%M%S"),userid=self.context["request"].user,randint_str=random.randint(10,99))
		return order_sn


	#字段序列化或者校验完成后，调用该方法
	def validate(self, attrs):
		attrs["order_sn"] = self.get_order_sn()
		return attrs


	class Meta:
		model = OrderInfo
		fields = "__all__"


#订单里面的商品
class OrderGoodsSerializer(serializers.ModelSerializer):
	#订单商品和商品简历一对一的关系
	goods = GoodsSerializer(many=False)
	class Meta:
		model = OrderGoods
		fields = "__all__"