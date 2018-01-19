# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, F, Sum
from django.db import connections
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError, transaction

from haystack.query import SearchQuerySet

from .models import Vote, Legislator_Vote
from search.models import Keyword
from standpoint.models import Standpoint, User_Standpoint
from search.views import keyword_list, keyword_been_searched, keyword_normalize
from .tasks import update_vote_index
from commontag.views import paginate


def votes(request):
    qs = Q(content=request.GET['keyword']) if request.GET.get('keyword') else Q()
    qs = qs & Q(conflict=True) if request.GET.get('conscience') else qs
    qs = qs & Q(tags_num__gt=0) if request.GET.get('has_tag') else qs
    qs = qs & Q(tags__in=[request.GET['tag']]) if request.GET.get('tag') else qs
    votes = SearchQuerySet().filter(qs).models(Vote).order_by('-date', 'vote_seq')
    votes = paginate(request, votes)
    keywords = [x.content for x in SearchQuerySet().filter(category__exact=2).models(Keyword).order_by('-hits')]
    standpoints = Standpoint.objects.values('title').annotate(pro_sum=Sum('pro')).order_by('-pro_sum').distinct()
    get_params = '&'.join(['%s=%s' % (x, request.GET[x]) for x in ['keyword', 'conscience', 'has_tag'] if request.GET.get(x)])
    return render(request, 'vote/votes.html', {'votes': votes, 'conscience': request.GET.get('conscience'), 'keyword': request.GET.get('keyword', ''), 'keyword_obj': keywords, 'hot_keyword': keywords[:5], 'hot_standpoints': standpoints[:5], 'get_params': get_params})

def vote(request, vote_id):

    vote = get_object_or_404(Vote.objects.select_related('sitting'), uid=vote_id)
    if request.user.is_authenticated():
        if request.POST:
            with transaction.atomic():
                if request.POST.get('keyword', '').strip():
                    standpoint_id = u'vote-%s-%s' % (vote_id, request.POST['keyword'].strip())
                    Standpoint.objects.get_or_create(uid=standpoint_id, title=request.POST['keyword'].strip(), vote_id=vote_id, user=request.user)
                    update_vote_index.delay(vote_id)
                elif request.POST.get('pro'):
                    User_Standpoint.objects.create(standpoint_id=request.POST['pro'], user=request.user)
                    Standpoint.objects.filter(id=request.POST['pro']).update(pro=F('pro') + 1)
                    update_vote_index.delay(vote_id)
                elif request.POST.get('against'):
                    User_Standpoint.objects.get(standpoint_id=request.POST['against'], user=request.user).delete()
                    Standpoint.objects.filter(id=request.POST['against']).update(pro=F('pro') - 1)
                    update_vote_index.delay(vote_id)

    standpoints_of_vote = Standpoint.objects.filter(vote_id=vote_id)\
                                            .order_by('-pro')
    if request.user.is_authenticated():
        standpoints_of_vote = standpoints_of_vote.extra(select={
            'have_voted': "SELECT true FROM standpoint_user_standpoint su WHERE su.standpoint_id = standpoint_standpoint.id AND su.user_id = %s" % request.user.id,
        },)
    standpoints = list(Standpoint.objects.filter(vote__isnull=False, pro__gt=0).values_list('title', flat=True).distinct())
    return render(request, 'vote/vote.html', {'vote': vote, 'keyword_obj': standpoints, 'standpoints_of_vote': standpoints_of_vote})
