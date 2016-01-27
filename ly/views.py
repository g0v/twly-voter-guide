# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.contrib import auth
from django.core.urlresolvers import reverse

from haystack.query import SearchQuerySet

from legislator.models import Legislator
from candidates.models import Candidates, Terms
from vote.models import Vote
from bill.models import Bill
from standpoint.models import Standpoint
from search.models import Keyword

def about(request):
    nvotes = Vote.objects.count()
    nbills = Bill.objects.count()
    return render(request, 'about.html', {'nvotes': nvotes, 'nbills': nbills})

def reference(request):
    return render(request, 'reference.html', {})

def home(request):
    if request.GET.get('name'):
        params = request.GET['name'].split(u' - ')
        q = Q(name=params[0]) if len(params) == 1 else Q(name=params[0], county=params[1])
        person = SearchQuerySet().filter(q).models(Terms)
        if person:
            return redirect(reverse('candidates:district', kwargs={"ad": person[0].ad, "county": person[0].county, "constituency": person[0].constituency}))
    if request.GET.get('keyword'):
        votes = SearchQuerySet().filter(content=request.GET['keyword']).models(Vote)
        bills_uid = [x.uid for x in SearchQuerySet().filter(content=request.GET['keyword']).models(Bill)]
        bills = Bill.objects.filter(uid__in=bills_uid)
    else:
        votes, bills = [], []
    keywords = [x.content for x in SearchQuerySet().models(Keyword).order_by('-hits')]
    names = [u'%s - %s' % (x.name, x.county) for x in SearchQuerySet().models(Terms)]
    standpoints = Standpoint.objects.values('title').annotate(pro_sum=Sum('pro')).order_by('-pro_sum').distinct()
    return render(request, 'home.html', {'votes': votes, 'bills': bills, 'keyword': request.GET.get('keyword', ''), 'keyword_obj': keywords, 'hot_keyword': keywords[:6], 'names': names, 'hot_standpoints': standpoints[:5]})

def logout(request):
    auth.logout(request)
    return redirect('home')
