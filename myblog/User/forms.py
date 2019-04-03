from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist

class LoginForm(forms.Form):
    username=forms.CharField(label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
    password=forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入3-30位用户名'}))
    email = forms.EmailField(label='邮箱',
                               widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入用邮箱'}))
    verifacation_code = forms.CharField(label='验证码', required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '点击"发送"发送验证码到邮箱'}))
    password = forms.CharField(label='请输入密码',
                               max_length=16,
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入6-16位密码'}))
    password_again = forms.CharField(label='请再输入一次密码',
                               max_length=30,
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再输入一次密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已经存在')
        else:return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已经存在')
        else:
            return email

    def clean_password_again(self):
        password=self.cleaned_data['password']
        password_again=self.cleaned_data['password_again']
        if password !=password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        else:
            return password_again

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label='新的昵称',max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入新的昵称'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)
    def clean_nickname_new(self):
        nickname_new=self.cleaned_data.get('nickname_new','').strip()
        if nickname_new == '':
            raise forms.ValidationError('昵称不能为空')
        return nickname_new

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data



class BingEmailForm(forms.Form):
    email=forms.EmailField(label='新的邮箱',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱地址'}))
    verifacation_code= forms.CharField(label='验证码',required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '点击"发送"发送验证码到邮箱'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BingEmailForm, self).__init__(*args, **kwargs)


    def clean_verifacation_code(self):
        verifacation_code=self.cleaned_data['verifacation_code']
        if verifacation_code=='':
            print(999)
            raise forms.ValidationError('验证码不能为空')

        return verifacation_code
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已经存在')
        return  email

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户未登录')
        # 判断用户是否已经绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('已经绑定邮箱')
        # 判断验证码是否正确
        code = self.request.session.get('bind_email_code', '')
        verifacation_code = self.cleaned_data.get('verifacation_code', '')
        if not (code != '' and verifacation_code == code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data






