# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class Candidates(models.Model):
    uid = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=100)
    former_names = ArrayField(
        models.CharField(max_length=100),
        null=True,
        default=None,
    )
    birth = models.DateField(blank=True, null=True)
    identifiers = JSONField(null=True)
    data = JSONField(null=True)

    def __unicode__(self):
        return self.name

class Terms(models.Model):
    id = models.CharField(max_length=70, primary_key=True)
    candidate = models.ForeignKey(Candidates)
    latest_term = models.ForeignKey('legislator.LegislatorDetail', blank=True, null=True)
    legislator = models.OneToOneField('legislator.LegislatorDetail', blank=True, null=True, related_name='elected_candidate')
    ad = models.IntegerField(db_index=True, )
    number = models.IntegerField(db_index=True, blank=True, null=True)
    priority = models.IntegerField(db_index=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    constituency = models.IntegerField(db_index=True)
    county = models.CharField(db_index=True, max_length=100)
    district = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    votes_percentage = models.CharField(max_length=100, blank=True, null=True)
    elected = models.NullBooleanField(db_index=True)
    contact_details = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    platform = models.TextField(blank=True, null=True)
    politicalcontributions = JSONField(null=True)
    councilor = JSONField(null=True)
    cec_data = JSONField(null=True)

    class Meta:
        index_together = ['ad', 'county', 'constituency']

    def __unicode__(self):
        return self.name
