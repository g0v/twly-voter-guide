# -*- coding: utf-8 -*-
from django.db import models


class Issue(models.Model):
    proposals = models.ManyToManyField('proposal.Proposal', through='Issue_Proposal',blank=True,null=True)
    votes = models.ManyToManyField('vote.Vote', through='Issue_Vote',blank=True,null=True)
    bills = models.ManyToManyField('bill.Bill', through='Issue_Bill',blank=True,null=True)
    keywords = models.ManyToManyField('search.Keyword',blank=True,null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000,blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    hits = models.IntegerField(default=0,blank=True,null=True)
    reference = models.CharField(max_length=200,blank=True,null=True)
    def __unicode__(self):
        return self.title

class Issue_Vote(models.Model):
    vote = models.ForeignKey('vote.Vote')
    issue = models.ForeignKey(Issue)
    weights = models.IntegerField(default=0)
    class Meta:
        ordering = ['-weights']

class Issue_Proposal(models.Model):
    proposal = models.ForeignKey('proposal.Proposal')
    issue = models.ForeignKey(Issue)
    weights = models.IntegerField(default=0)
    class Meta:
        ordering = ['-weights']

class Issue_Bill(models.Model):
    bill = models.ForeignKey('bill.Bill')
    issue = models.ForeignKey(Issue)
    weights = models.IntegerField(default=0)
    class Meta:
        ordering = ['-weights']

class IssueGroup(models.Model):
    issue = models.ForeignKey(Issue)
    group = models.CharField(max_length=200,blank=True,null=True)
    def __unicode__(self):
        return self.group
