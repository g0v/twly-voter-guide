# -*- coding: utf-8 -*-
import operator,re
from django.shortcuts import render
from django.db.models import F,Q
from proposal.models import Proposal
from search.models import Keyword
from search.views import keyword_list
from issue.models import Issue


def proposal(request,proposal_id):
    proposal = Proposal.objects.select_related().get(pk=proposal_id)
    return render(request,'proposal/proposal.html', {'proposal': proposal})

def proposals(request,keyword_url):
    keyword,proposal,error = None,None,False
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        proposal = Proposal.objects.filter(reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-sitting__date','-pk')
        if proposal:
            keyword_obj = Keyword.objects.filter(category=1, content=keyword)
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            elif not keyword_url:
                k = Keyword(content=keyword, category=1, valid=True, hits=1)
                k.save()
    else:
        proposal = Proposal.objects.all().order_by('-sitting__date','-pk')[:100]
    return render(request,'proposal/proposals.html', {'proposal':proposal,'keyword':keyword,'error':error,'keyword_obj':keyword_list(1)})

def proposals_related_to_issue(request,issue_id):
    keyword, proposal = None, None
    keyword = Issue.objects.values_list('title', flat=True).get(pk=issue_id)
    if issue_id:
        proposal = Proposal.objects.filter(issue_proposal__issue_id=issue_id).order_by('date','-pk')
    return render(request,'proposal/proposals.html', {'keyword':keyword,'proposal':proposal,'keyword_obj':keyword_list(1)})


