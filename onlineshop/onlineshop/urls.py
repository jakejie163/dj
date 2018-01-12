from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns( 
    path('rosetta/', include('rosetta.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('_(coupons)/', include('coupons.urls', namespace='coupons')),
    path('_(payment)/', include('payment.urls', namespace='payment')),
    path('_(cart)/', include('cart.urls', namespace='cart')),
    path('_(orders)/', include('orders.urls', namespace='orders')),
    path('', include('shop.urls', namespace='shop')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
