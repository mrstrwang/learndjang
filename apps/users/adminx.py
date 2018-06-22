import xadmin
from .models import VerifyCode
from xadmin import views


class GlobaSettings(object):
	site_title = '谷粒商店后台'
	site_footer = 'atguigu_shop'


class VerifyCodeAdmin(object):
	list_display = ['code','mobile','add_time']

#注册
xadmin.site.register(VerifyCode,VerifyCodeAdmin)

#注册全局配置
xadmin.site.register(views.CommAdminView,GlobaSettings)
