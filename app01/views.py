
import os,django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app02.settings")# project_name 项目名称
# django.setup()
from django.shortcuts import render,HttpResponse,redirect


from app01 import models
# Create your views here.
"""
我们现在写的视图函数 都必须有返回值
"""


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        res = models.Userinfo.objects.filter(username=username)  # select * from userinfo where username='jason' and password=123;
        user_obj = res.first()  # 取queryset第一个元素
        print(user_obj)
    return render(request,'login.html')

def reg(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_obj = models.Userinfo.objects.create(username=username,password=password)
        print(user_obj)
    return render(request,'register.html')

