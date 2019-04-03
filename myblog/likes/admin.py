from django.contrib import admin
from .models import LikeCount,LikeRecord
# Register your models here.
@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ['like_num']
@admin.register(LikeRecord)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ['user','like_time']