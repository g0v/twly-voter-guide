# -*- coding: utf-8 -*-
from django.shortcuts import render
from vote.models import Vote
from proposal.models import Proposal
from bill.models import Bill


def reference(request):
    return render(request,'reference/reference.html', {'current_url': 'http://twly.herokuapp.com'+request.get_full_path()})
