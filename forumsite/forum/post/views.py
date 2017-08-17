# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Item

class ItemListView(ListView):
    model = Item
    context_object_name = 'item_list'
    template_name = 'post/index.html'

class ItemDetailView(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'post/detail.html'

