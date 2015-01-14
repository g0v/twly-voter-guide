# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from legislator import views

ad = 8
urlpatterns = patterns('',
    url(r'^(?P<index>conscience_vote|notvote)/(?P<ad>[1-9])/$', views.index, name='index'),
    url(r'^(?P<index>conscience_vote|notvote)/$', views.index, {"ad": ad}, name='index'),
    url(r'^counties/(?P<ad>\d+)/$', views.counties, name='counties'),
    url(r'^counties/$', views.counties, {"ad": ad}, name='counties'),
    url(r'^committees/(?P<ad>\d+)/$', views.committees, name='committees'),
    url(r'^committees/$', views.committees, {"ad": ad}, name='committees'),
    url(r'^county/(?P<county>.+)/(?P<ad>\d+)/$', views.county, name='county'),
    url(r'^county/(?P<county>.+)/$', views.county, {"ad": ad}, name='county'),
    url(r'^committee/(?P<committee>.+)/(?P<ad>\d+)/$', views.committee, name='committee'),
    url(r'^committee/(?P<committee>.+)/$', views.committee, {"ad": ad}, name='committee'),
    url(r'^voter/(?P<legislator_id>\d+)/(?P<ad>\d+)/(?P<index>conscience)/$', views.voter_detail, name='voter_detail'),
    url(r'^voter/(?P<legislator_id>\d+)/(?P<ad>\d+)/$', views.voter_detail, {"index": ''}, name='voter_detail'),
    url(r'^biller/(?P<legislator_id>\d+)/(?P<ad>\d+)/$', views.biller_detail, name='biller_detail'),
    url(r'^personal_political_contributions/(?P<legislator_id>\d+)/(?P<ad>\d+)/$', views.personal_political_contributions, name='personal_political_contributions'),
    url(r'^platformer/(?P<legislator_id>\d+)/(?P<ad>\d+)/$', views.platformer_detail, name='platformer_detail'),
    url(r'^report/(?P<index>biller|conscience_vote|vote|ly)/(?P<ad>\d+)/$', views.chart_report, name='chart_report'),
    url(r'^report/(?P<index>biller|conscience_vote|vote|ly)/$', views.chart_report, {"ad": ''}, name='chart_report'),
    url(r'^report/political_contributions/(?P<index>\S+)/(?P<compare>\S+)/(?P<party>\S+)/$', views.political_contributions_report, name='political_contributions_report'),
)
