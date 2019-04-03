from django.shortcuts import render,render_to_response
from django.shortcuts import get_object_or_404
from . models import BlogType,Blog
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from read_statistics.utils import read_cookie_read_once
from User.forms import LoginForm
# Create your views here.

def comment_data(request,blogs_all_list):
    context = {}
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBERS)  # 每10页进行分页
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求，默认返回1)
    page_of_blogs = paginator.get_page(page_num)
    page_num = page_of_blogs.number
    page_range = list(range(max(page_num - 2, 1), page_num)) + list(
        range(page_num, min(paginator.num_pages, page_num + 2) + 1))
    if page_range[0] - 1 > 1:
        page_range.insert(0, '....')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if paginator.num_pages - page_range[-1] > 1:
        page_range.append('....')
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    blog_dates=Blog.objects.dates('create_time', 'month', order='DESC')
    blog_count_data={}
    for blog_date in blog_dates:
        blog_count=Blog.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month).count()
        blog_count_data[blog_date]=blog_count

    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_count_data
    return context
def blog_list(request):
    context={}
    blogs_all_list = Blog.objects.all()
    context = comment_data(request, blogs_all_list)
    # paginator=Paginator(blogs_all_list,2)#每10篇进行分页
    # page_num=request.GET.get('page',1)#获取url的页面参数（GET请求，默认返回1)
    # page_of_blogs = paginator.get_page(page_num)
    # page_num=page_of_blogs.number
    # page_range=list(range(max(page_num-2,1),page_num))+list(range(page_num,min(paginator.num_pages,page_num+2)+1))
    # if page_range[0]-1>1:
    #     page_range.insert(0,'....')
    # if page_range[0]!=1:
    #     page_range.insert(0,1)
    # if paginator.num_pages-page_range[-1]>1:
    #     page_range.append('....')
    # if page_range[-1]!=paginator.num_pages:
    #     page_range.append(paginator.num_pages)
    # content['page_range']=page_range
    # content['page_of_blogs']=page_of_blogs
    # content['blogs']=page_of_blogs.object_list
    # content['blog_types']=BlogType.objects.all()
    # content['blogs_date']=Blog.objects.dates('create_time','month',order='DESC')
    return render(request, 'blog/blog_list.html', context)
def blog_article(request,article_pk):
    context = {}
    blog = Blog.objects.get(pk=article_pk)
    read_cookie_key=read_cookie_read_once(request,blog)
    context['article'] = blog
    context['login_form'] = LoginForm()
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    response = render_to_response('blog/blog_article.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return render(request,'blog/blog_article.html',context)

def blog_type_article(request,type_pk):
    type_name=get_object_or_404(BlogType,pk=type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=type_name)
    context = comment_data(request, blogs_all_list)
    context['type_name']=type_name
    return render(request, 'blog/blog_type_article.html',context)
def blog_with_date(request,year,month):
    blogs_all_list=Blog.objects.filter(create_time__year=year,create_time__month=month)
    context = comment_data(request, blogs_all_list)
    context['blog_with_date']='%s年%s月' %(year,month)
    return render(request,'blog/blog_with_date.html',context)
