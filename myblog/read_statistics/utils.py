import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail
from django.db.models import Sum
from django.utils import timezone
from blog.models import Blog
def read_cookie_read_once(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key='%s_%s_read' %(ct.model,obj.pk)
    if not request.COOKIES.get(key) :#if  not request.COOKIES.get(key):错误 'NoneType' object has no attribute 'lower'
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)
        readnum,creat=ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
    date=timezone.now().date()
    # if ReadDetail.objects.filter(content_type=ct,object_id=obj.pk,data=timezone.now).count():
    #     readdetailnum=ReadDetail.objects.get(content_type=ct,object_id=obj.pk,data=timezone.now)
    # else:readdetailnum=ReadDetail(content_type=ct,object_id=obj.pk)
    readdetailnum, creat = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk,date_now=date)
    readdetailnum.read_num+=1
    readdetailnum.save()
    return key
def get_seven_days_read_date(content_type):
    today=timezone.now()
    read_nums=[]
    date_nums=[]
    for i in range(6,-1,-1):
        date=today-datetime.timedelta(days=i)
        date_nums.append(date.strftime('%m/%d'))#将时间数据转换成字符串类型的时间数据
        read_detail=ReadDetail.objects.filter(content_type=content_type,date_now=date)
        result=read_detail.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0 )
    return read_nums,date_nums
def get_hot_read_date(content_type):
    today = timezone.now()
    read_details=ReadDetail.objects.filter(content_type=content_type,date_now=today).order_by('-read_num')
    return read_details[:7]
def get_hot_for_7_days():
    today = timezone.now()
    date=today-datetime.timedelta(days=7)
    blogs=Blog.objects.filter(read_details__date_now__lt=today,read_details__date_now__gte=date).values('id','title')\
                                .annotate(read_num_sum=Sum('read_details__read_num'))\
                                .order_by('-read_num_sum')
    return blogs[:7]



