# -*- coding: utf-8 -*-
from django.conf.urls import url
from candidates import views

urlpatterns = [
    url(r'^$', views.counties, {"ad": 9}),
    url(r'^(?P<ad>\d+)/(?P<county>\S+)/(?P<constituency>\d+)/$', views.district, name='district'),
    url(r'^(?P<ad>\d+)/(?P<county>\S+)/$', views.districts, name='districts'),
    url(r'^(?P<ad>\d+)/$', views.counties, name='counties'),
    url(r'^pc/(?P<id>\S+)/$', views.political_contributions, name='political_contributions'),
]
