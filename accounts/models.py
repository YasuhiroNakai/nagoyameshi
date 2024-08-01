from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""
    is_subscribed = models.BooleanField(default=False, verbose_name='有料会員')
    cord_number = models.CharField(max_length=200,verbose_name='カードNo',null=True,blank=True)
    date_of_expiry = models.CharField(max_length=200, verbose_name='有効期限',null=True,blank=True)
    security_key = models.CharField(max_length=200, verbose_name='セキュリティキー',null=True,blank=True)

    class Meta:
        verbose_name_plural = 'CustomUser'