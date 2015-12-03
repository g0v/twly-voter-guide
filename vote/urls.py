from django.conf.urls import url
from vote import views

urlpatterns = [
    url(r'^$', views.votes, name='votes'),
    url(r'^(?P<vote_id>\S+)/$', views.vote, name='vote_detail'),
]
