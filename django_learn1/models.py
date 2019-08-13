from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField()
    def __str__(self):
        return self.btitle
class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField()
    hcontent = models.CharField(max_length=1000)
    hbook =  models.ForeignKey(BookInfo)
    def __str__(self):
        return self.hname
# class UserModels(AbstractUser):
#     nickname = models.CharField(max_length=20,verbose_name="用户昵称",null=True)
#     mobile = models.CharField(max_length=11, null=True, verbose_name='电话')
#     address = models.CharField(max_length=100, null=True, verbose_name='住址')
#     sex = models.CharField(max_length=10, null=True, verbose_name='性别')
#     head_img =  models.ImageField(upload_to="%y/%m",verbose_name="头像",null=True)
#
#     class Meta:
#         db_table = 'user'
#         verbose_name = '用户'
#         verbose_name_plural = verbose_name

#用户表
class User(models.Model):
    gender = (("male","男"),("female","女"))
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    gender_sex =models.CharField(max_length=10,choices=gender,default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email

    class Meta:
        ordering = ['c_time']
        verbose_name = "用户表"
        verbose_name_plural = "用户表"
class Comments_Note(models.Model):
    hname = models.ForeignKey('User',to_field="email",default="1@1.com")
    hcontent = models.CharField(max_length=1000)
    h_time = models.DateTimeField(auto_now=True)