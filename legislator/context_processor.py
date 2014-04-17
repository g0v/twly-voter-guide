# -*- coding: utf-8 -*-
from django.conf import settings
from legislator.models import LegislatorDetail
from committees.models import Legislator_Committees
from bill.models import Bill


def current_url(request):
    return {'current_url': settings.SITE_DOMAIN+request.get_full_path()}

def last_update_time(request):
    return {'last_update_time': '2014-03-01'}

def district_list(request):
    return {'district_list': [u'\u50d1\u5c45\u570b\u5916\u570b\u6c11', u'\u5168\u570b\u4e0d\u5206\u5340', u'\u5357\u6295\u7e23', u'\u53f0\u4e2d\u5e02', u'\u53f0\u5317\u5e02', u'\u53f0\u5357\u5e02', u'\u53f0\u6771\u7e23', u'\u5609\u7fa9\u5e02', u'\u5609\u7fa9\u7e23', u'\u57fa\u9686\u5e02', u'\u5b9c\u862d\u7e23', u'\u5c4f\u6771\u7e23', u'\u5c71\u5730\u539f\u4f4f\u6c11', u'\u5e73\u5730\u539f\u4f4f\u6c11', u'\u5f70\u5316\u7e23', u'\u65b0\u5317\u5e02', u'\u65b0\u7af9\u5e02', u'\u65b0\u7af9\u7e23', u'\u6843\u5712\u7e23', u'\u6f8e\u6e56\u7e23', u'\u82b1\u84ee\u7e23', u'\u82d7\u6817\u7e23', u'\u9023\u6c5f\u7e23', u'\u91d1\u9580\u7e23', u'\u96f2\u6797\u7e23', u'\u9ad8\u96c4\u5e02']}

def committee_list(request):
    return {'committee_list': [u'\u4ea4\u901a\u59d4\u54e1\u6703', u'\u5167\u653f\u59d4\u54e1\u6703', u'\u53f8\u6cd5\u53ca\u6cd5\u5236\u59d4\u54e1\u6703', u'\u5916\u4ea4\u53ca\u570b\u9632\u59d4\u54e1\u6703', u'\u6559\u80b2\u53ca\u6587\u5316\u59d4\u54e1\u6703', u'\u6559\u80b2\u6587\u5316\u59d4\u54e1\u6703', u'\u793e\u6703\u798f\u5229\u53ca\u885b\u751f\u74b0\u5883\u59d4\u54e1\u6703', u'\u7a0b\u5e8f\u59d4\u54e1\u6703', u'\u7d00\u5f8b\u59d4\u54e1\u6703', u'\u7d93\u6fdf\u59d4\u54e1\u6703', u'\u7d93\u8cbb\u7a3d\u6838\u59d4\u54e1\u6703', u'\u8ca1\u653f\u59d4\u54e1\u6703']}

def distinct_progress_of_bill(request):
    return {'distinct_progress_of_bill': Bill.objects.filter(last_action__isnull=False).values_list('last_action', flat=True).distinct('last_action')}

def party_list(request):
    return {'party_list': [u'\u4e2d\u570b\u570b\u6c11\u9ee8', u'\u53f0\u7063\u5718\u7d50\u806f\u76df', u'\u6c11\u4e3b\u9032\u6b65\u9ee8', u'\u7121\u9ee8\u5718\u7d50\u806f\u76df', u'\u7121\u9ee8\u7c4d', u'\u89aa\u6c11\u9ee8']}
