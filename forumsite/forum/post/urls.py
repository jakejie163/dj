from django.conf.urls import url

from .views import ItemListView, ItemDetailView 

urlpatterns = [
    url(r'^$', ItemListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', ItemDetailView.as_view(), name='detail'),
]
