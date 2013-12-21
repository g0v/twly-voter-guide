# -*- coding: utf-8 -*-
import operator,re
from django.shortcuts import render
from django.db.models import Count,F,Q
from legislator.models import Legislator
from vote.models import Vote,Legislator_Vote
from search.models import Keyword
from search.views import keyword_list
from issue.models import Issue


def votes(request,keyword_url,index='normal'):
    keyword, votes, error = None, None, False
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
        votes = Vote.objects.filter(query).order_by('-sitting__date','-pk')
    return render(request,'vote/votes.html', {'votes': votes,'index':index,'keyword':keyword,'error':error,'keyword_obj':keyword_list(2)})

def votes_related_to_issue(request,issue_id):
    keyword, votes, index = None, None, 'normal'
    keyword = Issue.objects.values_list('title', flat=True).get(pk=issue_id)
    if issue_id:
        votes = Vote.objects.filter(issue_vote__issue_id=issue_id).order_by('date','-pk')
    date_list = votes.values('date').distinct().order_by('-date')
    return render(request,'vote/votes.html', {'votes': votes,'index':index,'keyword':keyword,'keyword_obj':keyword_list(2),'date_list':date_list})

def vote_detail(request,vote_id):
    nvotes = Vote.objects.count()
    vote = Vote.objects.get(uid=vote_id)
    if vote:
        vote.hits = F('hits') + 1
        vote.save(update_fields=['hits'])
        vote_addup = Legislator_Vote.objects.filter(vote_id=vote_id,decision__isnull=False).values('decision').annotate(Count('legislator', distinct=True))
    return render(request,'vote/vote_detail.html', {'vote':vote,'nvotes':nvotes,'vote_addup': vote_addup})
