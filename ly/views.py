# -*- coding: utf-8 -*-
from django.shortcuts import render
from vote.models import Vote
from proposal.models import Proposal
from bill.models import Bill

def about(request):
    nvotes = Vote.objects.count()
    nproposals = Proposal.objects.count()
    nbills = Bill.objects.count()
    return render(request,'about.html', {'nvotes':nvotes,'nproposals':nproposals,'nbills':nbills})

def reference(request):
    return render(request,'reference.html', {})
