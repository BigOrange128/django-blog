from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    email = models.EmailField('邮箱', unique = True, error_messages={'unique':"该邮箱已被使用！"})
    class Meta(AbstractUser.Meta):
        pass
