from django.conf.urls import patterns, url
from bill import views

urlpatterns = patterns('',
    url(r'^$', views.bills, name='bills'),
)
