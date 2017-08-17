# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField("名字", max_length=30, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '类别'


class Item(models.Model):
    title = models.CharField("标题", max_length=100)
    body = models.TextField("内容")
    publish = models.DateTimeField("发布时间",auto_now_add=True)
    created = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                verbose_name="发布者")
    cat = models.ForeignKey(Category, verbose_name="类别")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "帖子"
        ordering = ('-publish',)


class Comment(models.Model):
    text = models.TextField("内容")
    publish = models.DateTimeField("评论时间",auto_now_add=True)
    created = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name="user_comments",
                                verbose_name="发布者")
    item = models.ForeignKey(Item, related_name="item_comments")

    class Meta:
        verbose_name = verbose_name_plural = '评论'
        ordering = ('-publish',)
