# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from vote.models import Vote,Legislator_Vote
from proposal.models import Legislator_Proposal
from bill.models import Legislator_Bill


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
