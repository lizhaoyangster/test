from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout


# 01注册
@csrf_exempt  # 关闭跨站请求伪造
def signup(request):
    # 注册页面
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    # 注册请求
    elif request.method == "POST":
        return_form = UserCreationForm(request.POST)
        if return_form.is_valid():
            user = return_form.save()
            login(request, user)
            return redirect('/manage/')
        else:
            form = UserCreationForm()
            return render(request, 'signup.html', {
                'form': form,
            })


# 登录
@csrf_exempt
def signin(request):
    form = AuthenticationForm()
    if request.method == "POST":
        return_form = AuthenticationForm(data=request.POST)
        print(return_form)
        if return_form.is_valid():
            user = return_form.get_user()
            login(request, user)
            next_url = request.POST.get('next')
            return redirect(next_url)

    next = request.GET.get('next')
    return render(request, 'signin.html', {
        'form': form,
        'next': next,
    })


# 退出登录
@csrf_exempt
def signout(request):
    logout(request)
    return redirect('/')
