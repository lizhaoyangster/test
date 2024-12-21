from django.urls import path
from . import views

# 用户模块子路由
urlpatterns = [
    path('signin/', views.signin),  # 登录
    path('signup/', views.signup),  # 注册
    path('signout/', views.signout),  # 退出
]
