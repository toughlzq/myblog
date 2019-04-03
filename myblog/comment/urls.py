from . import views
from django.urls import path

urlpatterns = [
    path(r'update_comment',views.update_comment,name='update_comment'),
]