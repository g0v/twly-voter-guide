from django.conf.urls import patterns, url
from about import views

urlpatterns = patterns('',
    # ex: /about
    url(r'^$', views.about, name='about'),
)
