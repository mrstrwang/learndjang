from datetime import datetime
from django.shortcuts import render, redirect
from rest_framework import viewsets, mixins, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Shop.settings import app_private_key_path,alipay_public_key_path
from .models import ShopingCart, OrderInfo, OrderGoods
from .serializers import ShopingCartSerializer, ShopingCartDetailSeralizer, OrderInfoDetailSerializer, OrderInfoSerializer
from utils.permissions import IsOwnerOrReadOnly
from utils.alipay import AliPay

# Create your views here.


class ShopingCartViewSet(viewsets.ModelViewSet):
	queryset = ShopingCart.objects.all()
	# 序列化器被get_serializer_class重写
	# serializer_class = ShopingCartSerializer
	permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
	# JWT认证
	authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
	lookup_field = 'goods_id'

	def get_serializer_class(self):
		if self.action == 'list':
			return ShopingCartDetailSeralizer
		else:
			return ShopingCartSerializer

	def get_queryset(self):
		return ShopingCart.objects.filter(user=self.request.user)


class OrderViewSet(mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
	# serializer_class = ShopingCartSerializer
	# 这个时候删除某个地址的时候就会验证是否是对应用户的地址--IsOwnerOrReadOnly
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
	# JWT认证
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	# 序列化器
	# serializer_class = OrderSerializer

	def get_serializer_class(self):
		if self.action == 'retrieve':
			return OrderInfoDetailSerializer
		else:
			return OrderInfoSerializer

	def get_queryset(self):
		# 过滤得到当前用户的订单列表
		return OrderInfo.objects.filter(user=self.request.user)

	# 重新改方法用户提交订单
	def perform_create(self, serializer):
		order = serializer.save()
		# 得到当前用户购物车所有信息
		shop_carts = ShopingCart.objects.filter(user=self.request.user)
		for shop_cart in shop_carts:
			# 把数据和OrderGoods对应起来
			order_goods = OrderGoods()
			# 订单
			order_goods.order = order
			# 商品
			order_goods.goods = shop_cart.goods
			# 商品数量
			order_goods.goods_num = shop_cart.nums
			# 保存订单和商品关联的Model
			order_goods.save()
			# 把该条信息在购车中删除--订单提交后，清空购物车
			shop_cart.delete()


#支付宝支付成功后回调的接口
class AlipayView(views.APIView):

	def get(self,request):
		"""处理支付宝返回的return_url"""
		print("get request==",request)
		process_dict = {}
		for key,value in request.GET.items():
			process_dict[key] = value

		print(process_dict)
		alipay = AliPay(
			appid="2016091300503705",
			# post请求
			app_notify_url="http://118.190.202.67:8000/alipay/return/",
			app_private_key_path=app_private_key_path,
			alipay_public_key_path=alipay_public_key_path,
			# 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
			debug=True,  # 默认False,
			# get请求
			return_url="http://118.190.202.67:8000/alipay/return/"
		)
		#把签名删除掉
		sign_type = process_dict.pop("sign",None)
		#如果是True,数据没有修改；False校验不通过
		verify_result = alipay.verify(process_dict, sign_type)
		print(verify_result)
		if verify_result:
			# 支付宝交易号
			trade_no = process_dict.get("trade_no",None)

			# 商品号，网站唯一商品号
			goods_sn = process_dict.get("out_trade_no",None)

			pay_status = process_dict.get("pay_status","TRADE_SUCCESS")

			# 查询订单
			exsited_orders = OrderInfo.objects.filter(order_sn=goods_sn)

			for exsited_order in exsited_orders:
				# 支付宝交易号
				exsited_order.trade_no = trade_no
				# 支付状态
				exsited_order.pay_status = pay_status
				# 支付时间
				exsited_order.pay_time = datetime.now()
				# 保存
				exsited_order.save()

			#返回支付成功状态
			# return Response("success")

			response = redirect("index")
			# 设置cookie
			response.set_cookie("nextPath", "pay", max_age=2)
			return response
		else:
			# 跳转到首页
			response = redirect("index")
			return response

	def post(self,request):
		""" 处理支付宝的notify_url"""
		print("post request==", request)

		process_dict = {}
		for key, value in request.POST.items():
			process_dict[key] = value

		print(process_dict)
		alipay = AliPay(
			appid="2016091300503705",
			# post请求
			app_notify_url="http://118.190.202.67:8000/alipay/return/",
			app_private_key_path=app_private_key_path,
			alipay_public_key_path=alipay_public_key_path,
			# 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
			debug=True,  # 默认False,
			# get请求
			return_url="http://118.190.202.67:8000/alipay/return/"
		)
		# 把签名删除掉
		sign_type = process_dict.pop("sign", None)
		# 如果是True,数据没有修改；False校验不通过
		verify_result = alipay.verify(process_dict, sign_type)
		print(verify_result)
		if verify_result:
			# 支付宝交易号
			trade_no = process_dict.get("trade_no", None)

			# 商品号，网站唯一商品号
			goods_sn = process_dict.get("out_trade_no", None)

			pay_status = process_dict.get("pay_status", "TRADE_SUCCESS")

			# 查询订单
			exsited_orders = OrderInfo.objects.filter(order_sn=goods_sn)

			for exsited_order in exsited_orders:
				# 支付宝交易号
				exsited_order.trade_no = trade_no
				# 支付状态
				exsited_order.pay_status = pay_status
				# 支付时间
				exsited_order.pay_time = datetime.now()

				# 保存
				exsited_order.save()

			# 返回支付成功状态
			# return Response("success")

			response = redirect("index")
			# 设置cookie
			response.set_cookie("nextPath", "pay", max_age=2)
			return response
		else:
			# 跳转到首页
			response = redirect("index")
			return response





