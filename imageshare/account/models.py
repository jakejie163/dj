# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='用户')
    date_of_birth = models.DateField('出生日期',blank=True, null=True)
    photo = models.ImageField('头像',upload_to='users/%Y/%m/%d', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '个人简介'
    
    def __unicode__(self):
        return '用户{}的个人简介'.format(self.user.username)

    
class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return '{} 关注 {}'.format(self.user_from, self.user_to)


User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))
