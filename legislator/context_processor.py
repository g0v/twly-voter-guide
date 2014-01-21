# -*- coding: utf-8 -*-
from django.conf import settings
from legislator.models import LegislatorDetail
from committees.models import Legislator_Committees
from bill.models import Bill


def current_url(request):
    return {'current_url': settings.SITE_DOMAIN+request.get_full_path()}
def last_update_time(request):
    return {'last_update_time':'2014-01-16'}
def district_list(request):
    return {'district_list':LegislatorDetail.objects.filter(ad=8).values_list('county', flat=True).distinct('county')}
def committee_list(request):
    return {'committee_list':Legislator_Committees.objects.filter(ad=8).values_list('committee', flat=True).distinct('committee')}
def distinct_progress_of_bill(request):
    return {'distinct_progress_of_bill':Bill.objects.filter(last_action__isnull=False).values_list('last_action', flat=True).distinct('last_action')}
