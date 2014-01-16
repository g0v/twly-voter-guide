# -*- coding: utf-8 -*-
import operator,re
from django.shortcuts import render
from django.db.models import Count, F, Q
from .models import Bill
from search.models import Keyword
from search.views import keyword_list
from issue.models import Issue


def bills(request, keyword_url, index):
    keyword, query = None, Q()
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        bills = Bill.objects.filter(reduce(operator.or_, (Q(abstract__icontains=x) | Q(summary__icontains=x) for x in keyword.split())))
        query = Q(reduce(operator.or_, (Q(abstract__icontains=x) | Q(summary__icontains=x) for x in keyword.split())))
        if bills:
            keyword_obj = Keyword.objects.filter(category=3,content=keyword.strip())
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            else:
                k = Keyword(content=keyword.strip(),category=3,valid=True,hits=1)
                k.save()
    if index == 'normal':
        bills = Bill.objects.filter(query, last_action__isnull=False).order_by('-last_action_at')[:100]
    elif index == 'rejected':
        bills = Bill.objects.filter(query & Q(ttsmotions__progress='退回程序')).annotate(totalNum=Count('ttsmotions__id')).filter(totalNum__gt=1).order_by('-totalNum')
    return render(request,'bill/bills.html', {'index':index, 'keyword_obj':keyword_list(3), 'keyword':keyword, 'bills':bills})

def bills_related_to_issue(request,issue_id):
    keyword, bills = None, None
    keyword = Issue.objects.values_list('title', flat=True).get(pk=issue_id)
    if issue_id:
        bills = Bill.objects.filter(issue_bill__issue_id=issue_id).order_by('date','-pk')
    return render(request,'bill/bills.html', {'keyword':keyword,'bills':bills,'keyword_obj':keyword_list(3)})

def bill_detail(request, bill_id, proposal_id):
    bill = Bill.objects.filter(billid=bill_id,proposalid=proposal_id)[0]
    return render(request,'bill/bill_detail.html', {'bill': bill})

