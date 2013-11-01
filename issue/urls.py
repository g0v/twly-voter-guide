from django.conf.urls import patterns, url
from issue import views

urlpatterns = patterns('',
    # ex: /issue/
    url(r'^$', views.issues, name='issues'),
    # ex: /issue/xxx
    url(r'^(?P<issue_id>\d+)/$', views.issue, name='issue'),
)
