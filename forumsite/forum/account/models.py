# -*- coding:UTF-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(verbose_name='出生日期', blank=True, null=True)
    photo = models.ImageField(verbose_name='照片', upload_to='users/%Y/%m/%d', blank=True)
    
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
