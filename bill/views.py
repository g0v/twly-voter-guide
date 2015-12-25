# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q

from haystack.query import SearchQuerySet

from .models import Bill
from commontag.views import paginate
from search.views import keyword_list


def bills(request):
    if request.GET.get('keyword'):
        bills_uid = [x.uid for x in SearchQuerySet().filter(content=request.GET['keyword']).models(Bill).order_by('-uid')]
        bills = Bill.objects.filter(uid__in=bills_uid)
    else:
        bills = Bill.objects.filter(ad=8)
    bills = paginate(request, bills)
    keywords = keyword_list(3)
    return render(request, 'bill/bills.html', {'bills': bills, 'keyword_obj': keywords, 'hot_keyword': keywords[:5], 'keyword': request.GET.get('keyword', '')})
