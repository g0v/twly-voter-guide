# -*- coding: utf-8 -*-
from django.db import models
import datetime 
from django.utils import timezone

class Legislator(models.Model):
    name = models.CharField(max_length=200)
    party = models.CharField(max_length=200,null=True)
    eleDistrict = models.CharField(max_length=200,null=True)
    district = models.CharField(max_length=200,null=True)
    districtDetail = models.CharField(max_length=200,null=True)
    committee = models.CharField(max_length=200,null=True)
    enable = models.NullBooleanField()
    enableSession = models.CharField(max_length=200)
    enabledate = models.DateField(null=True)
    disableReason = models.CharField(max_length=200,null=True)
    hits = models.IntegerField(null=True)
    facebook = models.URLField(max_length=200,null=True)
    wiki = models.URLField(max_length=200,null=True)
    officialsite = models.URLField(max_length=200,null=True)
    def __unicode__(self):
        return self.name   
    def _not_vote_count(self):
        ideal_vote_count = Vote.objects.filter(date__gte=self.enabledate).count()
        vote_count = Vote.objects.filter(voter__id=self.id).count()
        return ideal_vote_count - vote_count
    notvote = property(_not_vote_count)
    def _priproposer_count(self):
        return Legislator_Proposal.objects.filter(legislator_id=self.id,priproposer=True).count()
    npriproposer = property(_priproposer_count)
    def _biller_count(self):
        return Legislator_Bill.objects.filter(legislator_id=self.id).count()
    nbill = property(_biller_count)
    def _pribiller_count(self):
        return Legislator_Bill.objects.filter(legislator_id=self.id,priproposer=True).count()
    npribill = property(_pribiller_count) 
    def _conscience_vote_count(self):
        return Legislator_Vote.objects.filter(legislator_id=self.id,conflict=True).count()
    nconsciencevote = property(_conscience_vote_count)
    
class Politics(models.Model):
    legislator = models.ForeignKey(Legislator,null=True)
    politic = models.TextField(max_length=1000)
    category = models.IntegerField(null=True)
    party = models.CharField(max_length=200,null=True)
    def __unicode__(self):
        return self.politic
    
class FileLog(models.Model):
    session = models.CharField(max_length=200)
    date = models.DateTimeField()
    def __unicode__(self):
        return self.session

class Attendance(models.Model):
    legislator = models.ForeignKey(Legislator)
    date = models.DateField(null=True)
    sessionPrd = models.PositiveIntegerField(null=True)
    session = models.CharField(max_length=200)
    category = models.PositiveIntegerField(null=True)
    presentNum = models.IntegerField()
    unpresentNum = models.IntegerField()
    def __unicode__(self):
        return self.session
    
class Proposal(models.Model):    
    proposer = models.ManyToManyField(Legislator, through='Legislator_Proposal')
    committee = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    date = models.DateField(null=True)
    sessionPrd = models.PositiveIntegerField(null=True)
    session = models.CharField(max_length=200)
    approve = models.IntegerField(null=True)
    hits = models.IntegerField(null=True)
    likes = models.IntegerField(null=True)
    dislikes = models.IntegerField(null=True)
    def __unicode__(self):
        return self.content
    @property
    def sorted_proposer_set(self):
        return self.proposer.all().order_by('legislator_proposal__id')
    @property
    def primary_proposer(self):
        return self.proposer.filter(legislator_proposal__proposal_id=self.id,legislator_proposal__priproposer=True)
    
class Legislator_Proposal(models.Model):    
    legislator = models.ForeignKey(Legislator)
    proposal = models.ForeignKey(Proposal)
    priproposer = models.NullBooleanField()

class Vote(models.Model):    
    voter = models.ManyToManyField(Legislator, through='Legislator_Vote')
    content = models.TextField(max_length=1000)
    date = models.DateField(null=True)
    sessionPrd = models.PositiveIntegerField(null=True)
    session = models.CharField(max_length=200)
    hits = models.IntegerField(null=True)
    likes = models.IntegerField(null=True)
    dislikes = models.IntegerField(null=True)
    conflict = models.NullBooleanField()
    def __unicode__(self):
        return self.content
    def _vote_result(self):
        vote = Legislator_Vote.objects.filter(vote_id=self.id)
        if vote.filter(decision=1).count() < vote.filter(decision=-1).count():
            return True
        else:
            return False       
    disapprove = property(_vote_result)
    
class Legislator_Vote(models.Model):    
    legislator = models.ForeignKey(Legislator)
    vote = models.ForeignKey(Vote)
    decision = models.IntegerField(null=True)
    conflict = models.NullBooleanField()
    class Meta:
        ordering = ['-decision']

class Keyword(models.Model):    
    content = models.CharField(max_length=200)
    category = models.IntegerField()
    valid = models.BooleanField()
    hits = models.IntegerField()
    def __unicode__(self):
        return self.content

class Bill(models.Model):    
    proposer = models.ManyToManyField(Legislator,null=True, through='Legislator_Bill')
    billid = models.IntegerField()
    proposalid = models.IntegerField()
    law = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=100,null=True)
    motivation = models.TextField(max_length=500,null=True)
    description = models.TextField(max_length=1000,null=True)
    date = models.DateField(null=True)
    committee = models.CharField(max_length=50,null=True)
    sessionPrd = models.PositiveIntegerField(null=True)
    progress = models.CharField(max_length=50,null=True)
    hits = models.IntegerField(null=True,default=0)
    def __unicode__(self):
        return self.title
    @property
    def sorted_proposer_set(self):
        return self.proposer.all().order_by('legislator_bill__id')
    @property
    def primary_proposer(self):
        return self.proposer.filter(legislator_bill__bill_id=self.id,legislator_bill__priproposer=True)    
class Legislator_Bill(models.Model):    
    legislator = models.ForeignKey(Legislator)
    bill = models.ForeignKey(Bill)
    priproposer = models.NullBooleanField()

class BillDetail(models.Model):    
    bill = models.ForeignKey(Bill)
    article = models.CharField(max_length=100,null=True)
    before = models.TextField(max_length=3000,null=True)
    after = models.TextField(max_length=3000,null=True)
    description = models.TextField(max_length=1000,null=True)
    class Meta:
        ordering = ['id']    

class Issue(models.Model):
    proposals = models.ManyToManyField(Proposal, through='Issue_Proposal',blank=True,null=True)
    votes = models.ManyToManyField(Vote, through='Issue_Vote',blank=True,null=True)
    bills = models.ManyToManyField(Bill, through='Issue_Bill',blank=True,null=True)
    keywords = models.ManyToManyField(Keyword,blank=True,null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000,blank=True,null=True)
    date = models.DateField(blank=True,null=True)
    hits = models.IntegerField(default=0,blank=True,null=True)
    reference = models.CharField(max_length=200,blank=True,null=True)
    def __unicode__(self):
        return self.title
    
class Issue_Proposal(models.Model):    
    proposal = models.ForeignKey(Proposal)
    issue = models.ForeignKey(Issue)
    weights = models.IntegerField(default=0)
    class Meta:
        ordering = ['-weights']

class Issue_Vote(models.Model):    
    vote = models.ForeignKey(Vote)
    issue = models.ForeignKey(Issue)
    weights = models.IntegerField(default=0)
    class Meta:
        ordering = ['-weights']

class Issue_Bill(models.Model):    
    bill = models.ForeignKey(Bill)
    issue = models.ForeignKey(Issue)
    weights = models.IntegerField(default=0)
    class Meta:
        ordering = ['-weights']
        
class Keyword_Issue(models.Model):    
    keyword = models.ForeignKey(Keyword)
    issue = models.ForeignKey(Issue)
    weights = models.IntegerField(default=0)
    class Meta:
        ordering = ['-weights']

class IssueGroup(models.Model):
    issue = models.ForeignKey(Issue)
    group = models.CharField(max_length=200,blank=True,null=True)
    def __unicode__(self):
        return self.group

