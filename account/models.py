from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,unique=True,on_delete=None)
    birth = models.DateField(blank=True,null=True)
    phone = models.CharField(max_length=11,null=True)
    createTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return 'user {}'.format(self.user.username)