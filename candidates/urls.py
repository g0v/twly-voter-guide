# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from candidates import views

urlpatterns = patterns('',
    url(r'^$', views.counties, {"ad": 8}),
    url(r'^(?P<ad>\d+)/(?P<county>\S+)/(?P<constituency>\d+)/$', views.district, name='district'),
    url(r'^(?P<ad>\d+)/(?P<county>\S+)/$', views.districts, name='districts'),
    url(r'^(?P<ad>\d+)/$', views.counties, name='counties'),
    url(r'^political_contributions/(?P<uid>\S+)/(?P<ad>\d+)/$', views.political_contributions, name='political_contributions'),
)
