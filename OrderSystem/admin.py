from django.contrib import admin
from .models import Food, Foodtype, Order, OrderItem, Staff, Staff_Table

# 修改title和header
admin.site.site_title = '四川航空餐厅点餐系统后台管理系统'
admin.site.site_header = '四川航空餐厅点餐系统-SCAL'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['ID', 'citizenID', 'name', 'gender', 'born_date', 'phone', 'address']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    search_fields = ['ID', 'citizenID', 'name', 'gender', 'born_date', 'phone', 'address']
    # 设置排序方式
    ordering = ['ID']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['ID', 'title', 'amount', 'price', 'cost_time', 'foodType']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    search_fields = ['ID', 'title', 'amount', 'price', 'cost_time', 'foodType']
    # 设置排序方式
    ordering = ['ID']


@admin.register(Foodtype)
class FoodtypeAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['ID', 'name']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    search_fields = ['ID', 'name']
    # 设置排序方式
    ordering = ['ID']


@admin.register(Order)
class OrdertypeAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['ID', 'create_time', 'pay_time', 'is_pay', 'food_amount', 'total_price', 'table_id', 'comment',
                    'staff']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    search_fields = ['ID', 'create_time', 'pay_time', 'is_pay', 'food_amount', 'total_price', 'table_id', 'comment',
                     'staff']
    # 设置排序方式
    ordering = ['ID']


@admin.register(OrderItem)
class OrderItemtypeAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['orderID', 'foodID', 'amount', 'sum_price', 'status', 'start_cook_time', 'end_cook_time', 'comment',
                    'comment']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    search_fields = ['orderID', 'foodID', 'amount', 'sum_price', 'status', 'start_cook_time', 'end_cook_time',
                     'comment',
                     'comment']
    # 设置排序方式
    ordering = ['orderID']


@admin.register(Staff_Table)
class Staff_TableAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['ID', 'name', 'staff']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    search_fields = ['ID', 'name', 'staff']
    # 设置排序方式
    ordering = ['ID']
