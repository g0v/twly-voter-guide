# -*- coding: utf-8 -*-
from django.shortcuts import render
from vote.models import Vote
from proposal.models import Proposal
from bill.models import Bill

def about(request):
    nvotes = Vote.objects.count()
    nproposals = Proposal.objects.count()
    nbills = Bill.objects.count()
    return render(request,'about/about.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path(),'nvotes':nvotes,'nproposals':nproposals,'nbills':nbills})
