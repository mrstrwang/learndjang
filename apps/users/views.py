from django.db.models import Q
from django.contrib.auth.backends import ModelBackend,get_user_model
from rest_framework import status,viewsets,mixins
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_encode_handler,jwt_payload_handler
from .models import VerifyCode
from .serializers import CodeSerializer,UserRegSerializer
import random
from utils.yunpian import YunPian
import json
# Create your views here.

#等到用户信息
User = get_user_model()


class UserViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
	queryset = User.objects.all()
	serializer_class = UserRegSerializer #配置注册序列化

	#当用户注册登录时会有不显示数据的情况，因为缺少token和user
	def create(self, request, *args, **kwargs):
		print('=======')
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = self.perform_create(serializer)
		# 本质就是自动
		re_dict = serializer.data
		# 封装成字典
		payload = jwt_payload_handler(user)
		# 安装jwt封装token
		re_dict["token"] = jwt_encode_handler(payload)
		re_dict["name"] = user.name if user.name else user.username
		headers = self.get_success_headers(re_dict)
		print(re_dict)
		print(headers)
		return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		return serializer.save()


class CodeViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
	queryset = VerifyCode.objects.all()
	serializer_class = CodeSerializer

	def generating(self):
		random_str = []
		data = '1234567890'
		for a in range(4):
			random_str.append(random.choice(data))
		return ''.join(random_str)

	def create(self, request, *args, **kwargs):
		#得到序列化器
		serializer = self.get_serializer(data=request.data)
		#校验序列化器的字段
		serializer.is_valid(raise_exception=True)
		mobile = serializer.data['mobile']
		code = self.generating()
		yun_pian = YunPian('4f70824dde066067241393c80c291ea6')
		sms_status = yun_pian.send_msg(mobile,code)
		print(sms_status)
		print(type(sms_status))
		sms_status = json.loads(sms_status,)

		if sms_status['code'] == 0:
			verify_code = VerifyCode(code=code,mobile=mobile)
			verify_code.save()
			# 暂时注释掉
			# self.perform_create(serializer)
			# headers = self.get_success_headers(serializer.data)
			# print(headers)
			return Response({"mobile":mobile,"msg":sms_status["msg"]}, status=status.HTTP_201_CREATED)
		else:
			return Response({"mobile":mobile,"msg":sms_status["msg"]}, status=status.HTTP_400_BAD_REQUEST)


class CustomModelBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			print('usrname===',username,'password===',password)
			user = User.objects.get(Q(username=username)|Q(mobile=username))
			#校验密码
			if user.check_password(password):
				return user
		except Exception as e:
			print(e)
			return None

