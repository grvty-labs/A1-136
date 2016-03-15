from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^canvas/$', TemplateView.as_view(template_name='canvas.html')),
]
