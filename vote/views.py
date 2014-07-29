# -*- coding: utf-8 -*-
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from .models import Vote, Legislator_Vote
from search.views import keyword_list, keyword_been_searched, keyword_normalize


def votes(request, index='normal'):
    result = None
    if index == 'conscience':
        query = Q(conflict=True)
    else:
        query = Q()
    #--> 依表決結果分類
    if 'result' in request.GET:
        result = request.GET['result']
        query = query & Q(result=result)
    #<--
    keyword = keyword_normalize(request.GET)
    if keyword:
        votes = Vote.objects.filter(query & reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-sitting__date', 'vote_seq')
        if votes:
            keyword_been_searched(keyword, 2)
    else:
        votes = Vote.objects.filter(query).order_by('-sitting__date', 'vote_seq')
    return render(request,'vote/votes.html', {'votes': votes, 'index':index, 'keyword':keyword, 'result':result, 'keyword_obj':keyword_list(2)})

def vote(request, vote_id):
    data = None
    vote = Legislator_Vote.objects.select_related().filter(vote_id=vote_id).order_by('-decision', 'legislator__party')
    try:
        data = dict(Vote.objects.get(uid=vote_id).results)
        data.pop('total', None)
    except Exception, e:
        print e
        return HttpResponseRedirect('/')
    return render(request,'vote/vote.html', {'vote':vote, 'data':data})
