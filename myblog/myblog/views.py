from django.shortcuts import render,redirect
from read_statistics.utils import get_seven_days_read_date,get_hot_read_date,get_hot_for_7_days
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from blog.models import Blog

def home(request):
    content={}
    get_hot_for_7_days_data =cache.get('get_hot_for_7_days_data')
    if get_hot_for_7_days_data is None:
        get_hot_for_7_days_data=get_hot_for_7_days()
        cache.set('get_hot_for_7_days_data',get_hot_for_7_days_data,3600)
    ct = ContentType.objects.get_for_model(Blog)
    read_nums,date_nums=get_seven_days_read_date(content_type=ct)
    read_details=get_hot_read_date(ct)
    content['read_details']=read_details
    content['read_nums']=read_nums
    content['date_nums'] = date_nums
    content['get_hot_for_7_days']=get_hot_for_7_days_data
    return render(request,'home.html',content)
# def login(request):
#     # username=request.POST.get('username','')
#     # password=request.POST.get('password','')
#     # user=auth.authenticate(request,username=username,password=password)
#     # referer=request.META.get('HTTP_REFERER',reverse('home'))
#     # if user is not None:
#     #     auth.login(request,user)
#     #     return redirect(referer)
#     # else:
#     #     return render(request,'error.html',{'message':'登录密码或账户错误'})
#
#     if request.method=='POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():#判断是否有效
#             user=login_form.cleaned_data['user']
#             auth.login(request,user)
#             return redirect(request.GET.get('from',reverse('home')))
#     else:
#         login_form = LoginForm()
#     content = {}
#     content['login_form'] = login_form
#     return render(request, 'login.html', content)
#
# def register(request):
#     if request.method=='POST':
#         reg_form = RegForm(request.POST)
#         if reg_form.is_valid():
#             username = reg_form.cleaned_data['username']
#             email = reg_form.cleaned_data['email']
#             password = reg_form.cleaned_data['password']
#             User.objects.create_user(username,email, password)
#             user = auth.authenticate(request, username=username, password=password)
#             user.save()
#             auth.login(request, user)
#             return redirect(request.GET.get('from', reverse('home')))
#     else:
#         reg_form = RegForm()
#     content={}
#     content['reg_form']=reg_form
#     return render(request,'register.html',content)
#
# def login_for_medal(request):
#     data={}
#     print(121212)
#     login_form = LoginForm(request.POST)
#     if login_form.is_valid():  # 判断是否有效
#         user = login_form.cleaned_data['user']
#         auth.login(request, user)
#         data['status'] = 'SUCCESS'
#     else:
#         data['status']='ERROR'
#     return JsonResponse(data)
#
# def logout(request):
#     auth.logout(request)
#     return redirect(request.GET.get('from', reverse('home')))
#
# def user_info(request):
#
#     context={}
#     return render(request,'user_info.html',context)

# from django.contrib import auth
# from django.contrib.auth.models import User
# from  django.urls import reverse
# from django.http import JsonResponse
# from User.forms import LoginForm,RegForm
