from django.conf.urls import url

from . import views
from .feeds import LatestPostsFeed


urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.PostListView.as_view(), 
        name='post_list_by_tag'),

    url(r'^(?P<post_id>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
]
