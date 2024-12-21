from django.contrib import admin
from django.urls import path, include
from . import views
from OrderSystem import views as order_views

# 路由配置
urlpatterns = [
    path('', views.home),  # 主页
    path('admin/', admin.site.urls),  # 后台管理系统
    path('order/', include('OrderSystem.urls')),  # 订单管理
    path('accounts/', include('Accounts.urls')),  # 用户管理

    path('food_supplier/', order_views.food_supplier),  # 后厨
    path('manage/', include([
        path('', order_views.manage),  # 订单管理
        path('serving_table_list', order_views.getServingTableList),  # 餐位管理
        path('serving_order_item_list', order_views.getOrderItemList),  # 餐位点餐
        path('staff_charge_table', order_views.set_staff_charge_table),  # 餐位负责人管理
        path('delive_food', order_views.delive_food),  # 上菜
        path('cook', order_views.cook),  # 接单
        path('orders', order_views.orders),  # 订单
        path('staffs', order_views.staffs),  # 员工
        path('tables', order_views.tables),  # 餐位
        path('foods', order_views.foods),  # 菜品
        path('dark', order_views.dark),  # 删除菜品
    ])),
]
