from . import views
from django.urls import path

urlpatterns = [
    path(r'like_change',views.like_change,name='like_change'),
]