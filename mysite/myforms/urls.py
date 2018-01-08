from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'myforms'
urlpatterns = [
    path('your-name/', views.get_name),
    path('thanks/', TemplateView.as_view(template_name='myforms/thanks.html')),
]
