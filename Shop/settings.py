"""
Django settings for Shop project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os,sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'apps_extra'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dq#5%of+nm#^yf6y6*=f4z*0wlbzeuo)9=5%svyus4uz7r)+uw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USRE_MODEL = 'users.UserProfile'

# Application definition
import sys
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'DjangoUeditor',
    'goods.apps.GoodsConfig',
    'trade.apps.TradeConfig',
    'user_operation.apps.UserOperationConfig',
    'xadmin',
    'crispy_forms',
    'rest_framework',
    'django_filters', #过滤
    'corsheaders', #跨域请求
    'rest_framework.authtoken', #token认证的配置
    'social_django',

]

MIDDLEWARE = [
    #添加跨域求情中间件
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#允许跨域请求
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'Shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'shop',
        'USER': 'wangfan',
        'PASSWORD': 'wangfan1234',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

#添加用户models继承重写的，需要
AUTH_USER_MODEL = 'users.UserProfile'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

#做json的分页配置
REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}

AUTHENTICATION_BACKENDS = (
    'users.views.CustomModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.weibo.WeiboOAuth2',  # 微博登陆认证
    'social_core.backends.qq.QQOAuth2',  # QQ登录认证
    'social_core.backends.weixin.WeixinOAuth2',  # 微信登录认证
)

import datetime

JWT_AUTH = {

    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

#配置支付宝key路径
app_private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private.txt')
alipay_public_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_public_key.txt')
# 配置静态资源目录
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)
# 配置支付宝支付成功的回调
notify_url="http://39.104.172.113//alipay/return/"

SOCIAL_AUTH_STORAGE = 'social_django_mongoengine.models.DjangoStorage'

SOCIAL_AUTH_WEIBO_KEY = '3829953451'
SOCIAL_AUTH_WEIBO_SECRET = '6e9ad8a70dd0aeb213ec79864e0563fd'
#微信
# SOCIAL_AUTH_WEIXIN_KEY = 'foobar'
# SOCIAL_AUTH_WEIXIN_SECRET = 'bazqux'
#QQ
# SOCIAL_AUTH_QQ_KEY = 'foobar'
# SOCIAL_AUTH_QQ_SECRET = 'bazqux'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'