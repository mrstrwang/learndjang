import random, json
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend,get_user_model
from rest_framework import status,viewsets,mixins, permissions, authentication
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_encode_handler,jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import VerifyCode
from .serializers import CodeSerializer,UserRegSerializer,UserDetailSerializer
from utils.yunpian import YunPian

# Create your views here.

#等到用户信息
User = get_user_model()


class UserViewset(mixins.UpdateModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
	queryset = User.objects.all()
	# serializer_class = UserRegSerializer #配置注册序列化

	#动态序列化器
	def get_serializer_class(self):
		if self.action =='retrieve': #得到某个用户信息
			return UserDetailSerializer
		elif self.action == 'create':
			return	UserRegSerializer
		return UserDetailSerializer

	def get_object(self):
		return self.request.user

	authentication_classes = (authentication.SessionAuthentication,JSONWebTokenAuthentication)
	def get_permissions(self):
		if self.action == 'retrieve': #请求得到某个用户
			return [permissions.IsAuthenticated()]
		elif self.action == 'create':
			return []
		return [] #默认返回kong

	#当用户注册登录时会有不显示数据的情况，因为缺少token和user
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = self.perform_create(serializer)
		# 封装成字典
		payload = jwt_payload_handler(user)
		# 本质就是自动
		re_dict = serializer.data
		# 安装jwt封装token
		re_dict["token"] = jwt_encode_handler(payload)
		re_dict["name"] = user.name if user.name else user.username
		headers = self.get_success_headers(re_dict)

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

