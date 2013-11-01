from django.conf.urls import patterns, url
from vote import views

urlpatterns = patterns('',
    # ex: /vote/related_to_issue/xxx
    url(r'^related_to_issue/(?P<issue_id>\d+)/$', views.votes_related_to_issue, name='votes_related_to_issue'),
    # ex: /vote
    url(r'^(?P<index>normal|conscience)/(?P<keyword_url>.+)?$', views.votes, name='votes'),
    # ex: /vote/123
    url(r'^(?P<vote_id>\d+)/$', views.vote_detail, name='vote_detail'),
)
