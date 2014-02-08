# -*- coding: utf-8 -*-
import operator,re
from django.shortcuts import render
from django.db.models import F,Q
from .models import Proposal
from search.models import Keyword
from search.views import keyword_list, keyword_been_searched, keyword_normalize


def proposal(request,proposal_id):
    proposal = Proposal.objects.select_related().get(uid=proposal_id)
    return render(request,'proposal/proposal.html', {'proposal': proposal})

def proposals(request,keyword_url):
    keyword = keyword_normalize(request, keyword_url)
    if keyword:
        proposal = Proposal.objects.filter(reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-sitting__date')
        if proposal:
            keyword_been_searched(keyword, 1)
    else:
        proposal = Proposal.objects.all().order_by('-sitting__date')[:100]
    return render(request,'proposal/proposals.html', {'proposal':proposal, 'keyword':keyword, 'keyword_obj':keyword_list(1)})
