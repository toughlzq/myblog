from . import views
from django.urls import path

urlpatterns = [
    path(r'login', views.login, name='login'),
    path(r'logout', views.logout, name='logout'),
    path(r'login_for_medal', views.login_for_medal, name='login_for_medal'),
    path(r'register', views.register, name='register'),
    path(r'user_info', views.user_info, name='user_info'),
    path(r'changenickname', views.change_nickname, name='changenickname'),
    path(r'bindemail', views.bindemail, name='bindemail'),
    path(r'send_email', views.send_email, name='send_email'),
]