from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),

]
