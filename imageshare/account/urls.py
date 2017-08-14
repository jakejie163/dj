# -*- coding:UTF-8 -*-

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),

    # 个人关注系统
    url(r'^users/$', views.user_list, name='user_list'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),
    url(r'^users/(?P<username>[-\w]+)/$', views.user_detail, name='user_detail'),

]
