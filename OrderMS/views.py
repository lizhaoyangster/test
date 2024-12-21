from django.shortcuts import render


# 首页
def home(request):
    return render(request, 'home.html')


