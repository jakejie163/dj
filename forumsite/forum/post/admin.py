# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category, Item, Comment

admin.site.register(Category)

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish', 'created', 'cat']
    list_filter = ['publish', 'cat']
    list_search = ['title', 'body']
    inlines = [ CommentInline, ]


