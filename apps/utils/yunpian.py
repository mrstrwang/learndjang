import requests

class YunPian(object):
	def __init__(self,apikey):
		self.apikey = apikey
		self.send_msg_url = "https://sms.yunpian.com/v2/sms/single_send.json"

	def send_msg(self,mobile,code):
		data = {
			'apikey':self.apikey,
			'mobile':mobile,
			'text': "【杨光福】您的验证码是%s" % code
		}
		response = requests.post(self.send_msg_url,data=data)
		print(response)
		return response.text


if __name__ == '__main__':
	yunpian = YunPian("4f70824dde066067241393c80c291ea6")
	print(yunpian.send_msg('17600664748','6666'))