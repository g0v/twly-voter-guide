# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import F
from issue.models import Issue

def issues(request):
    issues = Issue.objects.select_related().order_by('-hits')
    issue = issues[0]
    return render(request,'legislator/issue.html', {'issues':issues,'issue':issue})

def issue(request,issue_id):
    issues = Issue.objects.select_related().order_by('-hits')
    issue = issues.get(pk=issue_id)
    if issue:
        issue.hits = F('hits') + 1
        issue.save(update_fields=['hits'])
    return render(request,'legislator/issue.html', {'issues':issues,'issue':issue})
