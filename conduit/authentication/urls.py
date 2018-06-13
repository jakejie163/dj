# -*- coding:UTF-8 -*-

from django.conf.urls import url

from .views import (
    RegistrationAPIView, 
    LoginAPIView, 
    UserRetrieveUpdateAPIView,
)

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),  #好像没有充分利用url的命名参数
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),
]
