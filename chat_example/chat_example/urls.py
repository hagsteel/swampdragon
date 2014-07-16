from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chat_example.views.home', name='home'),
    url(r'^$', include('chat_example.chat.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
