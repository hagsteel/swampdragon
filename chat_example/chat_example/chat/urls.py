from django.conf.urls import patterns, include, url
from chat_example.chat.views import ChatView

urlpatterns = patterns('',
    url(r'^$', ChatView.as_view(), name='home'),
)
