# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from legislator import views

urlpatterns = patterns('',
    url(r'^$', views.index, {"index": 'biller', "ad":''}),
    url(r'^(?P<index>biller|conscience_vote|committee|district|notvote)/(?P<ad>[1-9])/$', views.index, name='index'),
    url(r'^(?P<index>biller|conscience_vote|committee|district|notvote)/$', views.index, {"ad": ''}, name='index'),
    url(r'^district/(?P<index>.+)/(?P<ad>[1-9])/$', views.index_district, name='index_district'),
    url(r'^district/(?P<index>.+)/$', views.index_district, {"ad": ''}, name='index_district'),
    url(r'^committee/(?P<index>.+)/$', views.index_committee, name='index_committee'),
    url(r'^voter/(?P<legislator_id>\d+)/(?P<ad>[1-9])/(?P<index>conscience)/$', views.voter_detail, name='voter_detail'),
    url(r'^voter/(?P<legislator_id>\d+)/(?P<ad>[1-9])/$', views.voter_detail, {"index": ''}, name='voter_detail'),
    url(r'^voter/(?P<legislator_id>\d+)/(?P<index>conscience)?/?$', views.voter_detail, {"ad": ''}, name='voter_detail'),
    url(r'^voter/(?P<legislator_id>\d+)/$', views.voter_detail, {"index": '', "ad": ''}, name='voter_detail'),
    url(r'^biller/(?P<legislator_id>\d+)/$', views.biller_detail, name='biller_detail'),
    url(r'^personal_political_contributions/(?P<legislator_id>\d+)/(?P<ad>\d+)/$', views.personal_political_contributions, name='personal_political_contributions'),
    url(r'^personal_political_contributions/(?P<legislator_id>\d+)/$', views.personal_political_contributions, {"ad": ''}, name='personal_political_contributions'),
    url(r'^platform/(?P<legislator_id>\d+)/$', views.platformer_detail, name='platformer_detail'),
    url(r'^report/(?P<index>biller|conscience_vote|vote|ly)/(?P<ad>\d+)/$', views.chart_report, name='chart_report'),
    url(r'^report/(?P<index>biller|conscience_vote|vote|ly)/$', views.chart_report, {"ad": ''}, name='chart_report'),
    url(r'^report/political_contributions/(?P<index>\S+)/(?P<compare>\S+)/(?P<party>\S+)/$', views.political_contributions_report, name='political_contributions_report'),
)
