# -*- coding:UTF-8 -*-
# DEMO:
# 内部通用试图的钩子: get_queryset, get_context_data, get_object

from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    View, ListView, DetailView,
    FormView, CreateView, UpdateView, DeleteView,
)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

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


# 一个出版设的所有书
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


# mixin应用举例
class RecordInterest(SingleObjectMixin, View):
    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        #开始实际的记录了
        #
        #
        return HttpResponseRedirect(
                reverse('author-detail', kwargs={'pk': self.object.pk })
        )


# 一个出版设的所有书，感觉增加了复杂性
class PublisherBookList2(SingleObjectMixin, ListView):
    paginate_by = 2
    template_name = "books/books_by_publisher2.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Publisher.objects.all()) # 得到publisher
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  #Bug?这里到底是调用了哪一个的get_context_data?
        context['publisher'] = self.object # 上下文传递publisher
        return context

    def get_queryset(self):
        return self.object.book_set.all() #得到books



# 滥用GCBV增加复杂性的例子
#
# 功能：不仅展示author的detail,还增加了一个表单(处理)
# 解决方案一
class AuthorInterestForm(forms.Form):
    message = forms.CharField()

class AuthorDetail1(FormMixin, DetailView):
    model = Author
    form_class = AuthorInterestForm

    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk}) # 注意这里

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()  # 注意这里
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        # 增加一些自处理
        #
        return super().form_valid(form) # form_valid会重定向，但mix-in的重定向规则需要自己配置


# 解决方案二：写两个独立的类View，当普通函数调用
class AuthorDisplay(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AuthorInterestForm()
        return context


class AuthorInterest(SingleObjectMixin, FormView):
    template_name = 'books/author_detail.html'
    form_class = AuthorInterestForm
    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()     # 注意这里
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk})  # 自定义跳转的规则


class AuthorDetail2(View):
    def get(self, request, *args, **kwargs):
        view = AuthorDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AuthorInterest.as_view()
        return view(request, *args, **kwargs)
