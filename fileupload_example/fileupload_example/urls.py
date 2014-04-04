from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^nong/$', TemplateView.as_view(template_name='home_nong.html'), name='home_no_angular'),

    url(r'^admin/', include(admin.site.urls)),
)
