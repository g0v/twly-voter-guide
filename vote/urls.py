from django.conf.urls import patterns, url
from vote import views

urlpatterns = patterns('',
    url(r'^$', views.votes, name='votes'),
    url(r'^(?P<vote_id>\S+)/$', views.vote, name='vote_detail'),
)
