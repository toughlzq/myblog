from django.contrib import admin
from .models import BlogType,Blog
# Register your models here.
# admin.site.register(Blog,BlogType)
@admin.register(BlogType)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','auther','blog_type','read_num','create_time','last_update_time')