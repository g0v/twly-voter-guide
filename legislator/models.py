# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone
from json_field import JSONField
from vote.models import Vote,Legislator_Vote
from proposal.models import Legislator_Proposal
from bill.models import Legislator_Bill


class Legislator(models.Model):
    uid = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    former_names = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name   

class LegislatorDetail(models.Model):
    legislator = models.ForeignKey(Legislator, to_field="uid")
    ad = models.IntegerField()
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, blank=True, null=True)
    party = models.CharField(max_length=50, blank=True, null=True)
    caucus = models.CharField(max_length=50, blank=True, null=True)
    constituency = models.CharField(max_length=100)
    in_office = models.BooleanField()
    contacts = JSONField(null=True)
    term_start = models.DateField(blank=True, null=True)
    term_end = JSONField(null=True)
    education = models.TextField(max_length=1000, blank=True, null=True)
    experience = models.TextField(max_length=1000, blank=True, null=True)
    remark = models.TextField(max_length=200, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    social_media = JSONField(null=True)
    def __unicode__(self):
        return self.name
    def _not_vote_count(self):
        ideal_vote_count = Vote.objects.filter(date__gte=self.term_start).count()
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
