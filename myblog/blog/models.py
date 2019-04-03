from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNum,ReadNumExpandMethon,ReadDetail
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class BlogType(models.Model):
    type_name=models.CharField(max_length=20)
    def __str__(self):
        return self.type_name
class Blog(models.Model,ReadNumExpandMethon):
    title=models.CharField(max_length=30)
    contene=RichTextUploadingField()
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    auther=models.ForeignKey(User,on_delete=models.CASCADE)
    create_time=models.DateTimeField(auto_now_add=True)
    last_update_time=models.DateTimeField(auto_now=True)
    read_details = GenericRelation(ReadDetail)

    def __str__(self):
        return self.title
    class Meta:
        ordering=['-create_time']
