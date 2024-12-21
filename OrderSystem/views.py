from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Food, Foodtype, Order, OrderItem, Staff, Staff_Table
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import connection
from . import forms
import json
import datetime


# 01餐位下单
@csrf_exempt
def OrderHome(request):
    if request.method == "GET":
        foodList = Food.objects.all()
        foodTypeList = Foodtype.objects.all()
        tableList = Staff_Table.objects.all()
        return render(
            request,
            'OrderHome.html',
            {
                'foodList': foodList,
                'foodTypeList': foodTypeList,
                'tableList': tableList,
            }
        )
    elif request.method == "POST":
        foodList = json.loads(request.POST.get('foodList'))
        table_id = request.POST.get('table')

        # 创建订单 填写基本信息
        new_order = Order(table_id=table_id, is_pay=False)
        staff_in_charge = Staff_Table.objects.get(pk=table_id).staff
        new_order.staff = staff_in_charge  # 当前桌子的负责人
        new_order.save()

        # 先 save 再获取 ID
        order_id = new_order.ID
        food_amount = 0
        total_price = 0

        for food in foodList:
            curFood = Food.objects.get(pk=food['id'])
            price = curFood.price
            sum_price = price * food['amount']
            curFood.amount -= food['amount']
            curFood.save()

            food_amount += food['amount']
            total_price += sum_price

            OrderItem.objects.create(
                orderID=new_order,
                foodID=curFood,
                amount=food['amount'],
                sum_price=sum_price
            )
        # 订单的物品总数、总价
        new_order.food_amount = food_amount
        new_order.total_price = total_price
        new_order.save()

        return HttpResponse(json.dumps({
            'order_id': order_id
        }))


# 02账单详情页
def QueryOrder(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except:
        return HttpResponse('无此订单！')

    foodList = Food.objects.filter(orderitem__orderID__ID=order_id)

    with connection.cursor() as cursor:
        SELECT_COL = 'OrderSystem_food.ID ID, OrderSystem_food.title title, OrderSystem_orderitem.amount amount'
        SELECT_COL += ', OrderSystem_orderitem.sum_price '
        SELECT_COL += ', OrderSystem_orderitem.start_cook_time '
        SELECT_COL += ', OrderSystem_orderitem.end_cook_time '
        SELECT_FROM = 'OrderSystem_food, OrderSystem_orderitem '
        SELECT_WHERE = 'OrderSystem_food.ID=OrderSystem_orderitem.foodID_id '
        SELECT_WHERE += ' and OrderSystem_orderitem.orderID_id={0}'.format(
            order_id)
        cursor.execute(
            f'select {SELECT_COL} from {SELECT_FROM} where {SELECT_WHERE}')
        foodJsonList = dictfetchall(cursor)

    return render(request, 'QueryOrder.html', {
        'order': order,
        'foodList': foodJsonList,
    })


# 03待结账页面
def CheckUnpaidOrder(request):
    # 查询当前未结账订单
    orderList = []
    with connection.cursor() as cursor:
        SELECT_COL = 'ID, create_time, table_id, total_price'
        SELECT_FROM = 'OrderSystem_order'
        SELECT_WHERE = 'is_pay=0'  # 0 false
        SELECT = f'select {SELECT_COL} from {SELECT_FROM} where {SELECT_WHERE}'
        cursor.execute(SELECT)
        orderList = dictfetchall(cursor)
        print(orderList)

    return render(request, 'CheckUnpaidOrder.html', {
        'orderList': orderList,
    })


# 04结账
@csrf_exempt
def CheckOut(request):
    if request.method == "POST":
        order_list = json.loads(request.POST.get('order_list'))
        print(order_list)
        for order_data in order_list:
            print(order_data)
            order_id = order_data['order_id']
            is_pay = order_data['is_pay']

            if is_pay:
                order = Order.objects.get(pk=order_id)
                if order.is_pay:
                    print("已经支付！")
                    return HttpResponse(json.dumps({
                        'status': 'ALREADY_PAY'
                    }))

                order.is_pay = True
                order.pay_time = datetime.datetime.now()
                order.save()
            else:
                return HttpResponse(json.dumps({
                    'status': 'NO_PAY'
                }))

        return HttpResponse(json.dumps({
            'status': 'OK'
        }))


# 05管理界面（餐位管理人）
@login_required
def manage(request):
    staffList = Staff.objects.all()
    # (餐桌号 + 餐桌名字 + 负责人ID + 负责人姓名)
    tableInfoList = []
    with connection.cursor() as cursor:
        SELECT_COL = ' distinct {0}_staff_table.ID table_id '
        SELECT_COL += ', {0}_staff_table.name table_name '
        SELECT_COL += ', {0}_staff.ID staff_id '
        SELECT_COL += ', {0}_staff.name staff_name '
        SELECT_COL = SELECT_COL.format('OrderSystem')

        SELECT_FROM = '{0}_staff_table, {0}_staff '
        SELECT_FROM = SELECT_FROM.format('OrderSystem')

        SELECT_WHERE = '{0}_staff.ID = {0}_staff_table.staff_id '
        SELECT_WHERE = SELECT_WHERE.format('OrderSystem')

        SELECT_SQL = f'select {SELECT_COL} from {SELECT_FROM} where {SELECT_WHERE}'
        cursor.execute(SELECT_SQL)

        tableInfoList = dictfetchall(cursor)

    return render(request, 'manage.html', {
        'tableInfoList': tableInfoList,
        'staffList': staffList,
        'user': request.user,
    })


# 06 获取正在接受服务的餐位信息
@csrf_exempt
def getServingTableList(request):
    # (餐桌号 + 餐桌名字 + 负责人ID + 负责人姓名)
    servingTableList = []
    with connection.cursor() as cursor:
        SELECT_COL = 'distinct {0}_order.table_id table_id '
        SELECT_COL = SELECT_COL.format('OrderSystem')

        SELECT_FROM = '{0}_order '
        SELECT_FROM = SELECT_FROM.format('OrderSystem')

        SELECT_WHERE = '{0}_order.is_pay = 0 '  # false 0
        SELECT_WHERE = SELECT_WHERE.format('OrderSystem')

        SELECT_SQL = f'select {SELECT_COL} from {SELECT_FROM} where {SELECT_WHERE}'
        SELECT_SQL += 'order by table_id'
        cursor.execute(SELECT_SQL)

        servingTableInfoList = dictfetchall(cursor)
        for tableInfo in servingTableInfoList:
            servingTableList.append(tableInfo['table_id'])
    print(json.dumps(servingTableList))
    return HttpResponse(json.dumps({
        'servingTableList': servingTableList,
    }))


# 07后厨查看订单（接单或上菜）
@csrf_exempt
def getOrderItemList(request):
    if request.method == "POST":
        # 没有指定 order_id 就返回所有 order_item
        order_id = request.POST.get('order_id')
        print(order_id)
        with connection.cursor() as cursor:
            SELECT_COL = '{0}orderitem.orderID_id orderID_id '
            SELECT_COL += ',{0}order.table_id table_id '
            SELECT_COL += ',{0}orderitem.foodID_id foodID_id '
            SELECT_COL += ',{0}food.title food_name '
            SELECT_COL += ',{0}orderitem.amount food_amount '
            SELECT_COL += ',{0}orderitem.status status '
            SELECT_COL = SELECT_COL.format('OrderSystem_')

            SELECT_FROM = '{0}orderitem, {0}food, {0}order '
            SELECT_FROM = SELECT_FROM.format('OrderSystem_')

            SELECT_WHERE = 'foodID_id = {0}food.ID '
            SELECT_WHERE += ' and {0}order.ID = orderID_id '
            SELECT_WHERE += ' and {0}order.is_pay = 0 '
            SELECT_WHERE += (' and orderID_id=' +
                             order_id) if order_id != None else ''
            SELECT_WHERE = SELECT_WHERE.format('OrderSystem_')

            SELECT_SQL = f'select {SELECT_COL} from {SELECT_FROM} where {SELECT_WHERE}'
            SELECT_SQL += 'order by table_id'
            print(SELECT_SQL)
            '''
            select 
                OrderSystem_orderitem.orderID_id orderID_id ,
                OrderSystem_order.table_id table_id ,
                OrderSystem_orderitem.foodID_id foodID_id,
                OrderSystem_food.title food_name ,
                OrderSystem_orderitem.amount food_amount ,
                OrderSystem_orderitem.status status 
            from 
                OrderSystem_orderitem, OrderSystem_food, OrderSystem_order  
            where 
                foodID_id = OrderSystem_food.ID and OrderSystem_order.ID = orderID_id  and OrderSystem_order.is_pay = 0 order by table_id
            '''

            cursor.execute(SELECT_SQL)

            orderItemList = dictfetchall(cursor)
            json_data = json.dumps(orderItemList)
            print(json_data)
            return HttpResponse(json_data)


# 08更新餐桌表中的员工
@csrf_exempt
def set_staff_charge_table(request):
    if request.method == "POST":
        table_id = request.POST.get("table_id")
        staff_id = request.POST.get("staff_id")
        try:
            Staff_Table.objects.filter(pk=table_id).update(staff_id=staff_id)
            return HttpResponse(json.dumps({
                'status': "OK"
            }))
        except:
            return HttpResponse(json.dumps({
                'status': "FAIL"
            }))


# 09上菜
@csrf_exempt
def delive_food(request):
    print("上菜请求")
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        food_id = request.POST.get("food_id")
        print(order_id, food_id)
        OrderItem.objects.filter(orderID_id=order_id, foodID_id=food_id).update(status=3)
        try:
            return HttpResponse(json.dumps({
                'status': "OK"
            }))
        except:
            return HttpResponse(json.dumps({
                'status': "FAIL"
            }))


# 10后厨界面
@login_required
def food_supplier(request):
    return render(request, 'FoodSupplier.html')


# 11后厨接单或者呼叫上菜
@csrf_exempt
def cook(request):
    print(request.path)
    if request.method == "POST":
        OP = request.POST.get("OP")
        print("op=", OP)
        order_id = int(request.POST.get("order_id"))
        food_id = int(request.POST.get("food_id"))
        print(order_id, food_id)
        orderItem = OrderItem.objects.filter(orderID_id=order_id, foodID_id=food_id)
        print(orderItem)
        target_status = 1 if OP == "take_order" else 2

        if OP == "take_order":
            orderItem.update(status=target_status)
            orderItem.update(start_cook_time=datetime.datetime.now())
        else:
            orderItem.update(status=target_status)
            orderItem.update(end_cook_time=datetime.datetime.now())

        orderItem.save()

        return HttpResponse(json.dumps({
            'status': 'OK',
        }))


# 辅助函数 数据库查询结果转换成 json/dict'''
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# -------------管理功能 --------------
# 01订单管理
def orders(request):
    orders = Order.objects.all()
    return render(request, 'manage/orders.html', {
        'orders': orders,
    })


# 02员工管理
@csrf_exempt
def staffs(request):
    if request.method == "GET":
        form = forms.StaffForm()
        staffs = Staff.objects.all()
        return render(request, 'manage/staffs.html', {
            'form': form,
            'staffs': staffs,
        })
    elif request.method == "POST":
        form_back = forms.StaffForm(request.POST)
        if form_back.is_valid():
            form_back.save()
            return redirect('/manage/staffs')
        else:
            print(form_back.errors.as_data())
            print(form_back.errors.as_json())
            print(form_back.errors.as_text())
            print(form_back.errors.as_ul())
            return HttpResponse(json.dumps({
                'status': 'FAIL',
            }))


# 03餐位管理
@csrf_exempt
def tables(request):
    if request.method == "GET":
        print("get")
        form = forms.Staff_TableForm()
        tables = []
        staffs = []
        with connection.cursor() as cursor:
            SELECT_COL = ' distinct {0}_staff_table.ID table_id '
            SELECT_COL += ', {0}_staff_table.name table_name '
            SELECT_COL += ', {0}_staff.ID staff_id '
            SELECT_COL += ', {0}_staff.name staff_name '
            SELECT_COL = SELECT_COL.format('OrderSystem')

            SELECT_FROM = '{0}_staff_table, {0}_staff '
            SELECT_FROM = SELECT_FROM.format('OrderSystem')

            SELECT_WHERE = '{0}_staff.ID = {0}_staff_table.staff_id '
            SELECT_WHERE = SELECT_WHERE.format('OrderSystem')

            SELECT_SQL = f'select {SELECT_COL} from {SELECT_FROM} where {SELECT_WHERE}'
            cursor.execute(SELECT_SQL)

            tables = dictfetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute(
                'select ID staff_id, name staff_name from OrderSystem_staff;')
            staffs = dictfetchall(cursor)

        print(tables)

        return render(request, 'manage/tables.html', {
            'form': form,
            'tables': tables,
            'staffs': staffs,
        })
    elif request.method == "POST":
        print("post")
        form_back = forms.Staff_TableForm(request.POST)
        if form_back.is_valid():
            form_back.save()
            return redirect('/manage/tables')
        else:
            print(form_back.errors.as_data())
            print(form_back.errors.as_json())
            print(form_back.errors.as_text())
            print(form_back.errors.as_ul())
            return HttpResponse(json.dumps({
                'status': 'FAIL',
            }))


# 04菜品管理
@csrf_exempt
def foods(request):
    if request.method == "GET":
        foods = Food.objects.all()
        food_types = Foodtype.objects.all()
        food_form = forms.FoodForm()
        food_type_form = forms.FoodtypeForm()
        return render(request, 'manage/foods.html', {
            'food_form': food_form,
            'food_type_form': food_type_form,
            'foods': foods,
            'food_types': food_types,
        })
    elif request.method == "POST":
        form_food = forms.FoodForm(request.POST)
        form_food_type = forms.FoodtypeForm(request.POST)
        if form_food.is_valid():
            form_food.save()
            return redirect('/manage/foods')
        elif form_food_type.is_valid():
            form_food_type.save()
            return redirect('/manage/foods')
        else:
            return HttpResponse(json.dumps({
                'status': 'FAIL',
            }))


# 05删除菜品
@csrf_exempt
def dark(request):
    if request.method == "POST":
        target = request.POST

        table = target['table']
        SQL = ''
        if target['double'] == 'false':
            ID = target['id']
            SQL += f'delete from OrderSystem_{table} where ID={ID}'
        elif target['double'] == 'true':
            foodID_id = target['foodID_id']
            orderID_id = target['orderID_id']
            SQL += f'delete from OrderSystem_{table} where foodID_id={foodID_id} and orderID_id={orderID_id}'

        print('========================================================================')
        print(SQL)
        print('========================================================================')
        try:
            with connection.cursor() as cursor:
                cursor.execute(SQL)
            return HttpResponse(json.dumps({
                'status': 'OK',
            }))
        except:
            return HttpResponse(json.dumps({
                'status': 'FAIL',
            }))
