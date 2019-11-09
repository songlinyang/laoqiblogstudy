from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,unique=True,on_delete=None)
    birth = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=11,null=True)
    # createTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return 'user {}'.format(self.user.username)


class UserInfo(models.Model):
    user = models.OneToOneField(User,unique=True,on_delete=None) #对应用户
    school = models.CharField(max_length=100,blank=True) #毕业院校
    company = models.CharField(max_length=100,blank=True) # 所在公司
    profession = models.CharField(max_length=100,blank=True) # 专业
    address = models.CharField(max_length=100,blank=True) # 地址
    aboutme = models.TextField(blank=True) # 个人简介
    crateTime = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(max_length=1000,blank=True) #个人头像

    def __str__(self):
        return "User:{}".format(self.user.username)

