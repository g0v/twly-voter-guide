# -*- coding: utf-8 -*-
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count, Q
from .models import Bill
from search.views import keyword_list, keyword_been_searched, keyword_normalize


def bills(request, index):
    query = Q()
    keyword = keyword_normalize(request.GET)
    if keyword:
        bills = Bill.objects.filter(reduce(operator.or_, (Q(abstract__icontains=x) | Q(summary__icontains=x) for x in keyword.split())))
        query = Q(reduce(operator.or_, (Q(abstract__icontains=x) | Q(summary__icontains=x) for x in keyword.split())))
        if bills:
            keyword_been_searched(keyword, 3)
    if index == 'normal':
        progress = request.GET.get('progress', None)
        if progress:
            bills = Bill.objects.filter(query, last_action=progress).order_by('-last_action_at')
        else:
            bills = Bill.objects.filter(query, last_action__isnull=False).order_by('-last_action_at')[:100]
    elif index == 'rejected':
        bills = Bill.objects.filter(query & Q(ttsmotions__progress='退回程序')).annotate(totalNum=Count('ttsmotions__id')).filter(totalNum__gt=1).order_by('-totalNum')
    return render(request, 'bill/bills.html', {'index':index, 'keyword_obj':keyword_list(3), 'keyword':keyword, 'bills':bills})
