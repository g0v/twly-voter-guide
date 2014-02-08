# -*- coding: utf-8 -*-
import operator
from django.shortcuts import render
from django.db.models import Count, F, Q
from .models import Bill
from search.models import Keyword
from search.views import keyword_list, keyword_been_searched, keyword_normalize
from issue.models import Issue


def bills(request, keyword_url, index):
    query = Q()
    keyword = keyword_normalize(request, keyword_url)
    if keyword:
        bills = Bill.objects.filter(reduce(operator.or_, (Q(abstract__icontains=x) | Q(summary__icontains=x) for x in keyword.split())))
        query = Q(reduce(operator.or_, (Q(abstract__icontains=x) | Q(summary__icontains=x) for x in keyword.split())))
        if bills:
            keyword_been_searched(keyword, 3)
    if index == 'normal':
        bills = Bill.objects.filter(query, last_action__isnull=False).order_by('-last_action_at')[:100]
    elif index == 'rejected':
        bills = Bill.objects.filter(query & Q(ttsmotions__progress='退回程序')).annotate(totalNum=Count('ttsmotions__id')).filter(totalNum__gt=1).order_by('-totalNum')
    return render(request,'bill/bills.html', {'index':index, 'keyword_obj':keyword_list(3), 'keyword':keyword, 'bills':bills})

def bill_detail(request, bill_id, proposal_id):
    bill = Bill.objects.filter(billid=bill_id,proposalid=proposal_id)[0]
    return render(request,'bill/bill_detail.html', {'bill': bill})
