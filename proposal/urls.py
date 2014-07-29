from django.conf.urls import patterns, url
from proposal import views

urlpatterns = patterns('',
    # ex: /proposal/12
    url(r'^(?P<proposal_id>\S+)/$', views.proposal, name='proposal'),
    # ex: /proposal/related_to_issue/xxx
    #url(r'^related_to_issue/(?P<issue_id>\d+)/$', views.proposals_related_to_issue, name='proposals_related_to_issue'),
    # ex: /proposal/
    url(r'^$', views.proposals, name='proposals'),
)
