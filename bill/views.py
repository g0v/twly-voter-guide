# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q

from haystack.query import SearchQuerySet

from .models import Bill
from search.views import keyword_list


def bills(request):
    qs = Q(content=request.GET['keyword']) if request.GET.get('keyword') else Q()
    qs = qs & Q(last_action=request.GET['progress']) if request.GET.get('progress') else qs
    bills = SearchQuerySet().filter(qs).models(Bill).order_by('-last_action_at')
    bills = bills if len(qs) else bills[:10]
    keywords = keyword_list(3)
    return render(request, 'bill/bills.html', {'index': '', 'bills': bills, 'keyword_obj': keywords, 'hot_keyword': keywords[:5], 'keyword': request.GET.get('keyword', ''), 'progress': request.GET.get('progress', '')})
