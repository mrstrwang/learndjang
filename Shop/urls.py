"""Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
# from django.contrib import admin
import xadmin
from Shop.settings import MEDIA_ROOT
from django.views.static import serve
from goods.views import GoodsViewSet,CategoryViewSet
from users.views import CodeViewSet,UserViewset
from rest_framework.documentation import include_docs_urls
#终极版路由
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

# 路由器
router = DefaultRouter()
#注册路由器
router.register(r'goods', GoodsViewSet)
router.register(r'categorys',CategoryViewSet)
#注册短信验证路由
router.register(r'code',CodeViewSet,base_name='code')
#用户手机注册，要加上base_name 否则报错
router.register(r'users',UserViewset,base_name='users')


urlpatterns = [
	url(r'^xadmin/',xadmin.site.urls),
	url(r'media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
	url(r'docs/',include_docs_urls(title='硅谷商店')),
	url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
	#配置路由器，使其主页能看到api，点击到goods页面时也能看到api
	url(r'^',include(router.urls)),
	url(r'^api-token-auth/', views.obtain_auth_token),
	url(r'^login/', obtain_jwt_token)
]
