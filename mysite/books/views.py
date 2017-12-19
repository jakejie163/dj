# -*- coding:UTF-8 -*-
# DEMO:
# 内部通用试图的钩子: get_queryset, get_context_data, get_object

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Publisher, Book, Author


class PublisherList(ListView):
    model = Publisher
    context_object_name = 'books_publisher_list'


class PublisherDetail(DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()  #附加新的上下文
        return context


class BookList(ListView):
    queryset = Book.objects.order_by('-publication_date') # 过滤
    context_object_name = 'book_list'


class PublisherBookList(ListView):
    template_name = 'books/books_by_publisher.html'

    def get_queryset(self): #动态过滤，注意self参数保存了关键信息
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.publisher
        return context


class AuthorDetailView(DetailView):
    queryset = Author.objects.all()

    def get_object(self): # 增加额外的处理
        object = super().get_object()
        object.last_accessed = timezone.now()
        object.save()
        return object
