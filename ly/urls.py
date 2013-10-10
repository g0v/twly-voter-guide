from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework import routers
from api import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'legislator', views.LegislatorViewSet)
router.register(r'proposal', views.ProposalViewSet)
router.register(r'legislator_proposal', views.Legislator_ProposalViewSet)
router.register(r'vote', views.VoteViewSet)
router.register(r'legislator_vote', views.Legislator_VoteViewSet)
router.register(r'bill', views.BillViewSet)
router.register(r'legislator_bill', views.Legislator_BillViewSet)
router.register(r'bill_detail', views.BillDetailViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'politics', views.PoliticsViewSet)
router.register(r'issue', views.IssueViewSet)

urlpatterns = patterns('',
    url(r'^legislator/', include('legislator.urls', namespace="legislator")),
    url(r'', include('legislator.urls', namespace="legislator")),
    url(r'^api/', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Examples:
    # url(r'^$', 'ly.views.home', name='home'),
    # url(r'^ly/', include('ly.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)

