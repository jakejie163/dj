# -*- coding:UTF-8 -*-
# DEMO:
# 内部通用试图的钩子: get_queryset, get_context_data, get_object

from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    FormView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core.mail import send_mail

from reportlab.pdfgen import canvas 

from .models import Publisher, Book, Author
from .forms import ContactForm


# Publisher部分
class PublisherList(ListView):
    model = Publisher
    context_object_name = 'books_publisher_list'


class PublisherDetail(DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()   # 附加新的上下文
        return context


# Book部分
class BookList(ListView):
    queryset = Book.objects.order_by('-publication_date')   # 过滤
    context_object_name = 'book_list'

    def head(self, *args, **kwargs):    # 返回head信息，让client-api决定是否下载最新书籍信息
        last_book = self.get_queryset().latest('publication')
        response = HttpResponse('')
        response['Last-Modified'] = last_book.publication_date('%a, %d %b %Y\
%H:%M:%S GMT')
        return response


class PublisherBookList(ListView):
    template_name = 'books/books_by_publisher.html'

    def get_queryset(self):     # 动态过滤，注意self参数保存了关键信息
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.publisher
        return context


# Author部分
class AuthorList(ListView):
    model = Author


class AuthorDetailView(DetailView):
    queryset = Author.objects.all()

    def get_object(self):   # 增加额外的处理
        object = super().get_object()
        object.last_accessed = timezone.now()
        object.save()
        return object


@method_decorator(login_required, name='dispatch')
class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')


# 使用generic form view
class ContactView(FormView):
    template_name = 'books/contact_form.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


# 函数形式
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd['subject']
            message = cd['message']
            sender = cd['sender']
            cc_myself = cd['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)
            send_mail(subject, message, sender, recipients)

            return HttpResponseRedirect('/thanks/')
    else:
        form = ContactForm()
    return render(request, 'books/contact_form.html', {'form': form})


# 产生pdf文件
def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=file.pdf'

    p = canvas.Canvas(response)
    p.drawString(100, 100, 'Hello world.')
    p.showPage()
    p.save()
    return response
