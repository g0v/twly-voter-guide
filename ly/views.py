# -*- coding: utf-8 -*-
from django.shortcuts import render
from vote.models import Vote
from bill.models import Bill

def about(request):
    nvotes = Vote.objects.count()
    nbills = Bill.objects.count()
    return render(request,'about.html', {'nvotes': nvotes, 'nbills': nbills})

def reference(request):
    return render(request,'reference.html', {})
