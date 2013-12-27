from django.conf.urls import patterns, url
from legislator import views

urlpatterns = patterns('',
    # ex: /
    url(r'^$', views.index, {"index": 'biller'}),
    # ex: /legislator/
    url(r'^(?P<index>biller|conscience_vote|committee|district|notvote)?/$', views.index, name='index'),
    # ex: /legislator/district/
    url(r'^district/(?P<index>.+)$', views.index_district, name='index_district'),
    # ex: /legislator/committee/
    url(r'^committee/(?P<index>.+)$', views.index_committee, name='index_committee'),
    # ex: /legislator/5/
    url(r'^proposer/(?P<legislator_id>\d+)/(?P<keyword_url>.+)?$', views.proposer_detail, name='proposer_detail'),
    # ex: /legislator/voter/13
    url(r'^voter/(?P<legislator_id>\d+)/(?P<index>conscience)?/?(?P<keyword_url>.+)?$', views.voter_detail, name='voter_detail'),   
    # ex: /legislator/biller/113
    url(r'^biller/(?P<legislator_id>\d+)/?(?P<keyword_url>.+)?$', views.biller_detail, name='biller_detail'),
    # ex: /legislator/politics/113
    url(r'^platform/(?P<legislator_id>\d+)/$', views.ly_politics, name='ly_politics'),
    # ex: /legislator/report/
    url(r'^report/(?P<index>biller|conscience_vote|vote|proposal|ly|committee|ly_hit|nvote_gbdate)/$', views.chart_report, name='chart_report'),
    # ex: /legislator/personal_report/
    #url(r'^personal_report/(?P<legislator_id>\d+)/(?P<index>proposal|ly|vote)?/?$', views.chart_personal_report, name='chart_personal_report'),
)
