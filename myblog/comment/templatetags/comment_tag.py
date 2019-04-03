from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForms
register=template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type=ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type,object_id=obj.pk).count()
@register.simple_tag
def get_comment_forms(obj):
    content_type = ContentType.objects.get_for_model(obj)
    # 向form 表单中对应的input标签传入value值
    form=CommentForms(initial={'content_type': content_type.model, 'object_id': obj.pk,'reply_comment_id':0})
    return form
@register.simple_tag
def get_comments(obj):
    # 向blog_article.html页面传入评论数据
    content_type = ContentType.objects.get_for_model(obj)
    comments=Comment.objects.filter(content_type=content_type,object_id=obj.pk,parent=None)
    return comments.order_by('-comment_time')