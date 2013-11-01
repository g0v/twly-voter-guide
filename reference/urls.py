from django.conf.urls import patterns, url
from reference import views

urlpatterns = patterns('',
    # ex: /reference
    url(r'^$', views.reference, name='reference'),
)
