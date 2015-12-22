# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q

from haystack.query import SearchQuerySet

from .models import Bill
from search.views import keyword_list


def bills(request):
    qs = Q(content=request.GET['keyword']) if request.GET.get('keyword') else Q()
    bills_uid = [x.uid for x in SearchQuerySet().filter(qs).models(Bill).order_by('-uid')]
    bills_uid = bills_uid if len(qs) else bills_uid[:10]
    bills = Bill.objects.filter(uid__in=bills_uid)
    keywords = keyword_list(3)
    return render(request, 'bill/bills.html', {'bills': bills, 'keyword_obj': keywords, 'hot_keyword': keywords[:5], 'keyword': request.GET.get('keyword', '')})
