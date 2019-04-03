from . import views
from django.urls import path

urlpatterns = [
    path(r'',views.blog_list,name='blog_list'),
    path(r'<int:article_pk>/',views.blog_article,name='blog_article'),
    path(r'blog_type_article/<int:type_pk>',views.blog_type_article,name='blog_type_article'),
    path(r'date/<int:year><int:month>', views.blog_with_date, name='blog_with_date'),


]