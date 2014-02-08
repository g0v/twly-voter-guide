from django.conf.urls import patterns, url
from bill import views

urlpatterns = patterns('',
    # ex: /bill/related_to_issue/xxx
    #url(r'^related_to_issue/(?P<issue_id>\d+)/$', views.bills_related_to_issue, name='bills_related_to_issue'),
    # ex: /bill/xxx/yyyyy
    #url(r'^(?P<bill_id>\d+)/(?P<proposal_id>\d+)/$', views.bill_detail, name='bill_detail'),
    # ex: /bill
    url(r'^(?P<index>normal|rejected)/(?P<keyword_url>.+)?$', views.bills, name='bills'),
)
