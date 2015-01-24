# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework import routers
from api import views


#--> rest framework url
router = routers.DefaultRouter()
router.register(r'legislator', views.LegislatorViewSet)
router.register(r'legislator_terms', views.LegislatorDetailViewSet)
router.register(r'committees', views.CommitteesViewSet)
router.register(r'legislator_committees', views.Legislator_CommitteesViewSet)
router.register(r'sittings', views.SittingsViewSet)
router.register(r'vote', views.VoteViewSet)
router.register(r'legislator_vote', views.Legislator_VoteViewSet)
router.register(r'bill', views.BillViewSet)
router.register(r'legislator_bill', views.Legislator_BillViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'political_contributions', views.PoliticalContributionsViewSet)
#<--
urlpatterns = patterns('',
    url(r'^legislator/', include('legislator.urls', namespace="legislator")),
    url(r'^candidates/', include('candidates.urls', namespace="candidates")),
    url(r'^vote/', include('vote.urls', namespace="vote")),
    url(r'^bill/', include('bill.urls', namespace="bill")),
    url(r'^about/$', 'ly.views.about', name='about'),
    url(r'^reference/$', 'ly.views.reference', name='reference'),
    url(r'^$', 'candidates.views.counties', {'ad': 8}),
    url(r'^api/', include(router.urls)),
)
