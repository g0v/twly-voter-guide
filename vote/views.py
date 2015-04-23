# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db.models import Q, F

from haystack.query import SearchQuerySet

from .models import Vote, Legislator_Vote
from standpoint.models import Standpoint, User_Standpoint
from search.views import keyword_list, keyword_been_searched, keyword_normalize


def votes(request, index):
    qs = Q(content=request.GET['keyword']) if request.GET.get('keyword') else Q()
    qs = qs & Q(conflict=True) if index == 'conscience' else qs
    votes = SearchQuerySet().filter(qs).models(Vote).order_by('-date', 'vote_seq')
    keywords = keyword_list(2)
    return render(request, 'vote/votes.html', {'votes': votes, 'index': index, 'keyword': request.GET.get('keyword'), 'keyword_obj': keywords, 'hot_keyword': keywords[:5]})

def vote(request, vote_id):
    if request.GET:
        if not request.user.is_authenticated():
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        if request.GET.get('title'):
            Standpoint.objects.get_or_create(title=request.GET['title'], vote_id=vote_id)
        elif request.GET.get('standpoint_id'):
            obj, created = User_Standpoint.objects.get_or_create(standpoint_id=request.GET['standpoint_id'], user=request.user)
            if created:
                Standpoint.objects.filter(pk=request.GET['standpoint_id']).update(pro=F('pro') + 1)
    standpoints = Standpoint.objects.filter(vote_id=vote_id).order_by('-pro')
    decisions = Legislator_Vote.objects.select_related().filter(vote_id=vote_id).order_by('-decision', 'legislator__party')
    for decision in decisions:
        data = dict(decision.vote.results)
        data.pop('total', None)
        return render(request, 'vote/vote.html', {'vote': decisions, 'data': data, 'standpoints': standpoints})
    return redirect('vote:votes', index='normal')
