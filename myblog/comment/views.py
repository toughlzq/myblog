from .models import Comment
from django.http import JsonResponse
from .forms import CommentForms
from django.contrib.contenttypes.models import ContentType


# Create your views here.
def update_comment(request):

    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    # text=request.POST.get('text','')
    # if text.strip()=='':
    #     return render(request,'error.html',{'message':'评论内容为空','redirect_to':referer})
    # if not request.user.is_authenticated:
    #     return render(request,'error.html',{'message':'用户未登录','redirect_to':referer})
    # try:
    #     content_type = request.POST.get('content_type', '')
    #     object_id = int(request.POST.get('object_id', ''))
    #     model_class = ContentType.objects.get(model=content_type).model_class()
    #     # 获取对应的class对象此处为blog相当于from blog.models import blog
    #     model_obj = model_class.objects.get(pk=object_id)
    #     # 获取相应主键值的博客对象
    # except Exception as e :
    #     return render(request,'error.html',{'message':'评论对象不符合规定','redirect_to':referer})
    # comment=Comment()
    # comment.user=request.user
    # comment.text=text
    # comment.content_object=model_obj
    # comment.save()
    # return redirect(referer)
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    data = {}
    user = request.user
    comment_forms=CommentForms(request.POST,user=user)
    '''if comment_forms.is_valid():
        comment=Comment()
        comment.user=comment_forms.cleaned_data['user']
        comment.text=comment_forms.cleaned_data['text']
        comment.content_object=comment_forms.cleaned_data['content_object']
        parent=comment_forms.cleaned_data['parent']
        if not parent is None:
            comment.root=parent.root if not parent.root is None else parent
            comment.parent=parent
            comment.reply_to=parent.user
        comment.save()
        data['status']='SUCCESS'
        data['user']=user
        data['username']=comment.user.username
        data['comment_time']=localtime(comment.comment_time).strftime('%Y-%m-%d %H-%M-%S')
        data['text']=comment.text
        if not parent is None:
            data['reply_to']=comment.reply_to.username
        else:
            data['reply_to'] =''
        data['pk']=comment.pk
        data['root_pk']=comment.root.pk if not comment.root is None else ''

    else:
        data['status'] = 'ERROR'
        data['message']=list(comment_forms.errors.values())[0][0]
    return JsonResponse(data)'''
    if comment_forms.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.user = comment_forms.cleaned_data['user']
        comment.text = comment_forms.cleaned_data['text']
        comment.content_object = comment_forms.cleaned_data['content_object']

        parent = comment_forms.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_user()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_user()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data['status'] = 'ERROR'
        data['message'] = list(comment_forms.errors.values())[0][0]
    return JsonResponse(data)


