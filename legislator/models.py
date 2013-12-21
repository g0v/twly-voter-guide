# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone
from json_field import JSONField
from vote.models import Vote, Legislator_Vote
from proposal.models import Legislator_Proposal
from bill.models import Legislator_Bill
from committees.models import Committees


class Legislator(models.Model):
    uid = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    former_names = models.CharField(max_length=100, blank=True, null=True)
    def __unicode__(self):
        return self.name   

class LegislatorDetail(models.Model):
    legislator = models.ForeignKey(Legislator, to_field="uid")
    ad = models.IntegerField()
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(max_length=100, blank=True, null=True)
    caucus = models.CharField(max_length=100, blank=True, null=True)
    constituency = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    in_office = models.BooleanField()
    contacts = JSONField(null=True)
    term_start = models.DateField(blank=True, null=True)
    term_end = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    social_media = JSONField(null=True)
    hits = models.IntegerField()
    def __unicode__(self):
        return self.name

    def _not_vote_count(self):
        return Legislator_Vote.objects.filter(decision__isnull=True, legislator_id=self.id).count()
    notvote = property(_not_vote_count)

    def _conscience_vote_count(self):
        return Legislator_Vote.objects.filter(legislator_id=self.id,conflict=True).count()
    nconsciencevote = property(_conscience_vote_count)

    def _priproposer_count(self):
        return Legislator_Proposal.objects.filter(legislator_id=self.id,priproposer=True).count()
    npriproposer = property(_priproposer_count)

    def _biller_count(self):
        return Legislator_Bill.objects.filter(legislator_id=self.id).count()
    nbill = property(_biller_count)

    def _pribiller_count(self):
        return Legislator_Bill.objects.filter(legislator_id=self.id,priproposer=True).count()
    npribill = property(_pribiller_count) 

    def _current_committee(self):
        return Committees.objects.filter(legislator_committees__legislator_id=self.id).order_by('legislator_committees__session')[0].name
    current_committee = property(_current_committee) 

class Politics(models.Model):
    legislator = models.ForeignKey(Legislator, to_field="uid", blank=True, null=True)
    politic = models.TextField()
    category = models.IntegerField(blank=True, null=True)
    party = models.CharField(max_length=100, blank=True, null=True)
    def __unicode__(self):
        return self.politic
    
class FileLog(models.Model):
    sitting = models.CharField(unique=True, max_length=100)
    date = models.DateTimeField()
    def __unicode__(self):
        return self.session

class Attendance(models.Model):
    legislator = models.ForeignKey(LegislatorDetail)
    sitting = models.ForeignKey('sittings.Sittings', to_field="uid")
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    def __unicode__(self):
        return self.sitting
