from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord


register = template.Library()

@register.simple_tag
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return like_count.like_num

@register.simple_tag()
def get_like_status(obj,user):
    content_type =  ContentType.objects.get_for_model(obj)
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk,user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return str(content_type.model)