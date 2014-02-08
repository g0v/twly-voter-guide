# -*- coding: utf-8 -*-
import operator,re
from django.shortcuts import render
from django.db.models import Q
from .models import Vote, Legislator_Vote
from search.models import Keyword
from search.views import keyword_list, keyword_been_searched


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
            keyword_been_searched(keyword, 2)
    else:
        votes = Vote.objects.filter(query).order_by('-uid')
    return render(request,'vote/votes.html', {'votes': votes,'index':index,'keyword':keyword,'keyword_obj':keyword_list(2)})

def vote(request, vote_id):
    data = None
    vote = Legislator_Vote.objects.select_related().filter(vote_id=vote_id).order_by('-decision', 'legislator__party')
    if vote:
        data = dict(vote[0].vote.results)
        data.pop('total')
    return render(request,'vote/vote.html', {'vote':vote, 'data':data})
