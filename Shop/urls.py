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
from rest_framework.documentation import include_docs_urls
#终极版路由
from rest_framework.routers import DefaultRouter

# 路由器
router = DefaultRouter()
router.register(r'goods', GoodsViewSet)
router.register(r'categorys',CategoryViewSet)

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
	url(r'^xadmin/',xadmin.site.urls),
	url(r'media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
	# url(r'^goods/',GoodsListView.as_view(),name='goods_list'),
	url(r'docs/',include_docs_urls(title='硅谷商店')),
	url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
	#配置路由器，使其主页能看到api，点击到goods页面时也能看到api
	url(r'^',include(router.urls)),
]
