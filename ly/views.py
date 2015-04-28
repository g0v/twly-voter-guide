# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import auth

from haystack.query import SearchQuerySet

from vote.models import Vote
from bill.models import Bill
from search.models import Keyword

def about(request):
    nvotes = Vote.objects.count()
    nbills = Bill.objects.count()
    return render(request, 'about.html', {'nvotes': nvotes, 'nbills': nbills})

def reference(request):
    return render(request, 'reference.html', {})

def home(request):
    results = SearchQuerySet().filter(content=request.GET['keyword']).models(Vote, Bill) if request.GET.get('keyword') else []
    keywords = [x.content for x in SearchQuerySet().models(Keyword).order_by('-hits')]
    return render(request, 'home.html', {'results': results, 'keyword': request.GET.get('keyword'), 'keyword_obj': keywords, 'hot_keyword': keywords[:6]})

def logout(request):
    auth.logout(request)
    return redirect('home')
