from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/', include('articles.urls', namespace='articles')),
    url(r'^api/', include('authentication.urls', namespace='authentication')),
    url(r'^api/', include('profiles.urls', namespace='profiles')),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
