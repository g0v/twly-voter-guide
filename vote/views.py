# -*- coding: utf-8 -*-
import operator,re
from django.shortcuts import render
from django.db.models import Count,F,Q
from .models import Vote, Legislator_Vote
from search.models import Keyword
from search.views import keyword_list
from issue.models import Issue


def votes(request, keyword_url, index='normal'):
    keyword = None
    if index == 'conscience':
        query = Q(conflict=True)
    else:
        query = Q()
    if 'keyword' in request.GET:
        keyword = re.sub(u'[，。／＼、；］［＝－＜＞？：＂｛｝｜＋＿（）！＠＃％＄︿＆＊～~`!@#$%^&*_+-=,./<>?;:\'\"\[\]{}\|()]',' ',request.GET['keyword']).strip()
    elif keyword_url:
        keyword = keyword_url.strip()
    if keyword:
        votes = Vote.objects.filter(query & reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-sitting__date','-pk')
        if votes:
            keyword_obj = Keyword.objects.filter(category=2,content=keyword)
            if keyword_obj:
                keyword_obj.update(hits=F('hits')+1)
            elif not keyword_url:
                k = Keyword(content=keyword,category=2,valid=True,hits=1)
                k.save()
    else:
        votes = Vote.objects.filter(query).order_by('-uid')
    return render(request,'vote/votes.html', {'votes': votes,'index':index,'keyword':keyword,'keyword_obj':keyword_list(2)})

def vote(request, vote_id):
    vote = Legislator_Vote.objects.select_related().filter(vote_id=vote_id).order_by('-decision', 'legislator__party')
    data = dict(vote[0].vote.results)
    data.pop('total')
    return render(request,'vote/vote.html', {'vote':vote, 'data':data})
