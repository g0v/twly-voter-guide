# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db.models import Q

from haystack.query import SearchQuerySet

from .models import Vote, Legislator_Vote
from search.views import keyword_list, keyword_been_searched, keyword_normalize


def votes(request, index):
    qs = Q(content=request.GET['keyword']) if request.GET.get('keyword') else Q()
    qs = qs & Q(conflict=True) if index == 'conscience' else qs
    votes = SearchQuerySet().filter(qs).models(Vote).order_by('-date', 'vote_seq')
    keywords = keyword_list(2)
    return render(request, 'vote/votes.html', {'votes': votes, 'index': index, 'keyword': request.GET.get('keyword'), 'keyword_obj': keywords, 'hot_keyword': keywords[:5]})

def vote(request, vote_id):
    decisions = Legislator_Vote.objects.select_related().filter(vote_id=vote_id).order_by('-decision', 'legislator__party')
    for decision in decisions:
        data = dict(decision.vote.results)
        data.pop('total', None)
        return render(request, 'vote/vote.html', {'vote': decisions, 'data': data})
    return HttpResponseRedirect(reverse('vote:votes', kwargs={'index': 'normal'}))
