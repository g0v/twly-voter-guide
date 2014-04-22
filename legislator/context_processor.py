# -*- coding: utf-8 -*-
from django.conf import settings
from legislator.models import LegislatorDetail
from committees.models import Legislator_Committees
from bill.models import Bill


def current_url(request):
    return {'current_url': settings.SITE_DOMAIN+request.get_full_path()}

def last_update_time(request):
    return {'last_update_time':'2014-03-01'}

def district_list(request):
    return {'district_list':LegislatorDetail.objects.filter(ad=8).values_list('county', flat=True).distinct('county')}

def committee_list(request):
    return {'committee_list':Legislator_Committees.objects.filter(ad=8).values_list('committee', flat=True).distinct('committee')}

def distinct_progress_of_bill(request):
    return {'distinct_progress_of_bill':Bill.objects.filter(last_action__isnull=False).values_list('last_action', flat=True).distinct('last_action')}

def party_list(request):
    return {'party_list':LegislatorDetail.objects.filter(ad=8).values_list('party', flat=True).distinct('party')}

def property_category(request):
    return {'property_category':[u'航空器', u'現金', u'存款', u'債券', u'基金受益憑證', u'其他有價證券', u'具有相當價值之財產', u'保險', u'債權', u'債務', u'事業投資']}
