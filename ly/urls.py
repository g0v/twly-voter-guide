# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings
from rest_framework import routers

from . import views as ly_views
from api import views as api_views

#--> rest framework url
router = routers.DefaultRouter()
router.register(r'legislator', api_views.LegislatorViewSet)
router.register(r'legislator_terms', api_views.LegislatorDetailViewSet)
router.register(r'committees', api_views.CommitteesViewSet)
router.register(r'legislator_committees', api_views.Legislator_CommitteesViewSet)
router.register(r'sittings', api_views.SittingsViewSet)
router.register(r'vote', api_views.VoteViewSet)
router.register(r'legislator_vote', api_views.Legislator_VoteViewSet)
router.register(r'bill', api_views.BillViewSet)
router.register(r'legislator_bill', api_views.Legislator_BillViewSet)
router.register(r'attendance', api_views.AttendanceViewSet)
router.register(r'candidates', api_views.CandidatesViewSet)
router.register(r'candidates_terms', api_views.Candidates_TermsViewSet)
#<--
urlpatterns = [
    url(r'^$', ly_views.home, name='home'),
    url(r'^legislator/', include('legislator.urls', namespace="legislator")),
    url(r'^candidates/', include('candidates.urls', namespace="candidates")),
    url(r'^vote/', include('vote.urls', namespace="vote")),
    url(r'^bill/', include('bill.urls', namespace="bill")),
    url(r'^about/$', ly_views.about, name='about'),
    url(r'^reference/$', ly_views.reference, name='reference'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/logout/$', ly_views.logout, name='logout'),
    url(r'^api/', include(router.urls)),
]
