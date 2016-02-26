# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from haystack.query import SearchQuerySet

from .models import Bill, Law
from commontag.views import paginate
from search.views import keyword_list


def bills(request):
    if request.GET.get('keyword'):
        bills_uid = [x.uid for x in SearchQuerySet().filter(content=request.GET['keyword']).models(Bill)]
        bills = Bill.objects.filter(uid__in=bills_uid).prefetch_related('laws').order_by('-uid')
    else:
        bills = Bill.objects.all().prefetch_related('laws').order_by('-uid')
    bills = paginate(request, bills)
    keywords = keyword_list(3)
    get_params = '&'.join(['%s=%s' % (x, request.GET[x]) for x in ['keyword'] if request.GET.get(x)])
    return render(request, 'bill/bills.html', {'bills': bills, 'keyword_obj': keywords, 'hot_keyword': keywords[:5], 'keyword': request.GET.get('keyword', ''), 'get_params': get_params})

def bill(request, bill_id):
    law = get_object_or_404(Law.objects.select_related('bill'), bill_id=bill_id)
    return render(request, 'bill/law.html', {'law': law, })
