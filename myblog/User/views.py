from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from  django.urls import reverse
from django.http import JsonResponse
from User.forms import LoginForm,RegForm,ChangeNicknameForm,BingEmailForm
from .models import Profile
import random,string,time
from django.core.mail import send_mail

def login(request):

    if request.method=='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():#判断是否有效
            user=login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()
    content = {}
    content['login_form'] = login_form
    return render(request, 'User/login.html', content)

def register(request):
    if request.method=='POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            User.objects.create_user(username,email, password)
            user = auth.authenticate(request, username=username, password=password)
            user.save()
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    content={}
    content['reg_form']=reg_form
    return render(request,'User/register.html',content)

def login_for_medal(request):
    data={}
    print(121212)
    login_form = LoginForm(request.POST)
    if login_form.is_valid():  # 判断是否有效
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status']='ERROR'
    return JsonResponse(data)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context={}
    return render(request,'User/user_info.html',context)

def change_nickname(request):
    return_to=request.GET.get('from', reverse('home'))
    if request.method=='POST':
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new=form.cleaned_data['nickname_new']
            profile_user,created=Profile.objects.get_or_create(user=request.user)
            profile_user.nickname=nickname_new
            profile_user.save()
            return redirect(return_to)
    else:
        form=ChangeNicknameForm()
    context={}
    context['return_to_url']= return_to
    context['page_title']='修改昵称'
    context['sub_text']='修改'
    context['form_title']='修改昵称'
    context['form']=form
    return render(request, 'User/form.html', context)

def bindemail(request):
    return_to = request.GET.get('from', reverse('home'))
    if request.method=='POST':
        form = BingEmailForm(request.POST,request=request)
        if form.is_valid():
            email=form.cleaned_data['email']
            request.user.email=email
            request.user.save()
            return redirect(return_to)
    else:
        form=BingEmailForm()
    context={}
    context['form']=form
    context['return_to_url'] = return_to
    context['page_title'] = '绑定邮箱'
    context['sub_text'] ='绑定'
    context['form_title'] = '绑定邮箱'
    return render(request,'user/bind_email.html',context)

def send_email(request):
    email=request.GET.get('email','')
    data = {}
    if email !='':
        code=''.join(random.sample(string.ascii_letters+string.digits,4))

        now=int(time.time())
        send_code_time=request.session.get('send_code_time',0)
        if now-send_code_time<30:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now
            #发送邮件
            send_mail(
                '发送验证码',
                '验证码: %s' % code,
                '1517131558@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status']='ERROR'
    return JsonResponse(data)