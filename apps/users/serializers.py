from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
import re
from datetime import datetime,timedelta
from .models import VerifyCode

User = get_user_model()

class CodeSerializer(serializers.Serializer):

	mobile = serializers.CharField(max_length=11)

	def validate_mobile(self,mobile):
		if User.objects.filter(mobile=mobile).count():
			raise serializers.ValidationError('用户已经存在')

		if not re.match(r"1[3456789]\d{9}$",mobile):
			raise serializers.ValidationError("您输入的电话号码有误")

		#频次校验,1分钟一次
		one_minu_ago = datetime.now() -timedelta(minutes=1)
		if VerifyCode.objects.filter(mobile=mobile,add_time__gt=one_minu_ago).count():
			raise serializers.ValidationError("当前手机号码一分钟后才能发验证码")
		return mobile


class UserRegSerializer(serializers.ModelSerializer):
	# 最短不能低于4和答应4，不要反回给客户端
	code = serializers.CharField(label='验证码',max_length=4,min_length=4,required=True,write_only=True,error_messages={
		'length':'验证码长度应为4'},help_text='验证码')
	username = serializers.CharField(label="用户名", required=True, allow_blank=False,validators=[UniqueValidator(queryset=User.objects.all())])
	password = serializers.CharField(label='密码',style={'input_type':'password'},write_only=True)

	def create(self, validated_data):
		print('==========')
		user = super(UserRegSerializer, self).create(validated_data=validated_data)
		user.set_password(validated_data["password"])
		# 保存user对象
		user.save()
		return user

	def validate(self, attrs):
		attrs['mobile'] = attrs['username']
		del attrs['code']
		return attrs

	# 验证码不存在
	def validate_code(self, code):
		verify_codes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')

		if verify_codes:
			last_record = verify_codes[0]
			five_mintes_age = datetime.now() - timedelta(minutes=5)

			if last_record.add_time < five_mintes_age:
				raise serializers.ValidationError('验证码过期了')
			#校验验证码
			if last_record.code != code:
				raise serializers.ValidationError('验证码错误')
		else:
			raise serializers.ValidationError('验证码错误')


	class Meta:
		model = User
		fields = ('username','code','mobile','password')


