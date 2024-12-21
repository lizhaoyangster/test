import os

# 项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 项目密钥
SECRET_KEY = '#8jlxak#p673&-(x*)(d-)ideae3=+8(c&=uckz1hbvc7tu7c1'

# 调试模式
DEBUG = True

# 授权主机
ALLOWED_HOSTS = []

# 注册app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'OrderSystem',  # 点餐系统
    'Accounts',  # 用户管理
]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 主路由
ROOT_URLCONF = 'OrderMS.urls'

# 模板文件配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'OrderMS.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'db_order',  # 创建的数据库用户名
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 密码
        'HOST': '172.21.254.200',  # 主机
        'PORT': '4888',  # 数据库使用的端口
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# 密码验证
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

# 国际化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# 登录路由配置
LOGIN_URL = '/accounts/signin/'

# 静态文件 (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join('static'),)
