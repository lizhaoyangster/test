from django.urls import path, re_path
from . import views

# 订单子路由
urlpatterns = [
    path('', views.OrderHome, name='OrderHome'),
    path('check', views.CheckUnpaidOrder),
    path('checkout', views.CheckOut),
    re_path(r'q(?P<order_id>[\d]+)', views.QueryOrder),
]
