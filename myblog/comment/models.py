from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.contrib.auth.models import User
# Create your models here.

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text=models.TextField()
    comment_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)

    root = models.ForeignKey('self',related_name='root_comment',null= True,on_delete=models.CASCADE,blank=True)
    parent = models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.CASCADE,blank=True)
    reply_to= models.ForeignKey(User,related_name='replies',null=True,on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return self.text
    class Meta:
        ordering=['comment_time']