from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    url(r'^account/', include('account.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^post/', include('post.urls', namespace='post'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
