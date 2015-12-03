# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import JSONField


class Bill(models.Model):
    proposer = models.ManyToManyField('legislator.LegislatorDetail', through='Legislator_Bill')
    uid = models.TextField(primary_key=True)
    ad = models.IntegerField(db_index=True, )
    api_bill_id = models.TextField(unique=True)
    abstract = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    bill_type = models.TextField(blank=True, null=True)
    doc = JSONField(null=True)
    proposed_by = models.TextField(blank=True, null=True)
    sitting_introduced = models.TextField(blank=True, null=True)
    last_action_at = models.DateField(db_index=True, blank=True, null=True)
    last_action = models.TextField(db_index=True, blank=True, null=True)
    def __unicode__(self):
        return self.uid

class Legislator_Bill(models.Model):
    legislator = models.ForeignKey('legislator.LegislatorDetail', related_name='bills')
    bill = models.ForeignKey(Bill)
    priproposer = models.NullBooleanField(db_index=True, )
    petition = models.NullBooleanField(db_index=True, )

class ttsMotions(models.Model):
    bill = models.ForeignKey(Bill)
    sitting_id = models.TextField(blank=True, null=True)
    agencies = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    chair = models.TextField(blank=True, null=True)
    date = models.DateField()
    memo = models.TextField(blank=True, null=True)
    motion_type = models.TextField(blank=True, null=True)
    progress = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    source = JSONField(null=True)
    speakers = JSONField(null=True)
    summary = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    topic = models.TextField(blank=True, null=True)
    tts_key = models.TextField(blank=True, null=True)

class BillMotions(models.Model):
    bill = models.ForeignKey(Bill)
    sitting = models.ForeignKey('sittings.Sittings')
    agenda_item = models.IntegerField(blank=True, null=True)
    committee = models.TextField(blank=True, null=True)
    item = models.TextField(blank=True, null=True)
    motion_class = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
