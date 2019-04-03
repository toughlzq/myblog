# from django.shortcuts import render
# from django.http import JsonResponse
# from django.contrib.contenttypes.models import ContentType
# from .models import LikeRecord,LikeCount
# # Create your views here.
# def ErrorResponse(code,message):
#     data={}
#     data['status']='ERROR'
#     data['code']=code
#     data['message']=message
#     return JsonResponse(data)
# def SuccessResponse(like_count):
#     data={}
#     data[' like_count']= like_count
#     data['status']='SUCCESS'
#     return JsonResponse(data)
# def like_change(request):
#     is_like=request.GET.get('is_like')
#     if not request.user.is_authenticated:'
#         return ErrorResponse(404,'你还没有登录')
#     content_type = request.GET.get('content_type')
#     object_id = int(request.GET.get('object_id'))
#     try:
#         content_type = ContentType.objects.get(model=content_type)
#         model_class = content_type.model_class()
#         model_obj = model_class.objects.get(pk=object_id)
#     except:
#         return ErrorResponse(403, '对象不存在')
#     if request.GET.get('is_like') == 'true':
#         # 要点赞
#         like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
#                                                                 user=user)
#         if created:
#             # 未点赞过，进行点赞
#             like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
#             like_count.liked_num += 1
#             like_count.save()
#             return SuccessResponse(like_count.liked_num)
#         else:
#             # 已点赞过，不能重复点赞
#             return ErrorResponse(402, 'you were liked')
#     else:
#         # 要取消点赞
#         if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
#             # 有点赞过，取消点赞
#             like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
#             like_record.delete()
#             # 点赞总数减1
#             like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
#             if not created:
#                 like_count.liked_num -= 1
#                 like_count.save()
#                 return SuccessResponse(like_count.liked_num)
#             else:
#                 return ErrorResponse(404, 'data error')
#         else:
#             # 没有点赞过，不能取消
#             return ErrorResponse(403, 'you were not liked')


    # if is_like =='true':
    #     #需要点赞
    #     liked,created=LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=request.user)
    #     if created:
    #         #没有该user的点赞信息，创建LikeRecord模型的对象，
    #         liked.save()
    #         like_count,create=LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
    #         like_count.like_num+=1
    #         like_count.save()
    #         return SuccessResopnse(like_count)
    #     else:
    #         #有该user的点赞信息，出现错误
    #         return ErrorMessage(400,'你已经点赞过了')
    # else:
    #     #取消点赞
    #     if LikeRecord.objects.filter(content_type=content_type, object_id=object_id,user=request.user).exists():
    #         liked=LikeRecord.objects.get(content_type=content_type, object_id=object_id,user=request.user)
    #         liked.delete()
    #         like_count, create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
    #         if  not create:
    #             like_count.like_num-=1
    #             like_count.save()
    #             return SuccessResopnse(like_count)
    #         else:
    #             return ErrorMessage(401,'没有点赞数据')
    #     else:
    #         return ErrorMessage(402,'你还没有点赞')

from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)

def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'you were not login')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')

    # 处理数据
    if request.GET.get('is_like') == 'true':
        # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return SuccessResponse(like_count.like_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(402, 'you were liked')
    else:
        # 要取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数减1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.like_num -= 1
                like_count.save()
                return SuccessResponse(like_count.like_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            # 没有点赞过，不能取消
            return ErrorResponse(403, 'you were not liked')