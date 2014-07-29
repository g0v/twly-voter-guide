from django.conf.urls import patterns, url
from bill import views

urlpatterns = patterns('',
    url(r'^(?P<index>normal|rejected)/$', views.bills, name='bills'),
)
