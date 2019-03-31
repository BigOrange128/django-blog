from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import RegisterForm
from django.contrib import messages
# Create your views here.

def register(request):
    #.get方法，当第一个参数无法找到时，返回第二个参数的值
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == "POST":
        #生成表单实例
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '注册成功！已登录当前注册账号！')
            #自动登录注册的账号
            auth_login(request, user)
            if redirect_to:
                #返回传递的页面
                return redirect(redirect_to)
            else:
                #返回首页
                return redirect('/')
    else:
        #生成空表单
        form = RegisterForm()
    return render(request, 'blog/register.html', context={'form':form, 'next':redirect_to})
