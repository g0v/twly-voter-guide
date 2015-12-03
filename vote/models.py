# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import JSONField


class Vote(models.Model):
    voter = models.ManyToManyField('legislator.LegislatorDetail', through='Legislator_Vote')
    uid = models.CharField(max_length=32, primary_key=True)
    sitting = models.ForeignKey('sittings.Sittings', related_name='votes')
    vote_seq = models.CharField(max_length=10)
    category = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    conflict = models.NullBooleanField()
    result = models.CharField(blank=True, null=True, max_length=50)
    results = JSONField(null=True)
    def __unicode__(self):
        return self.uid

class Legislator_Vote(models.Model):
    legislator = models.ForeignKey('legislator.LegislatorDetail', related_name='votes')
    vote = models.ForeignKey(Vote)
    decision = models.IntegerField(db_index=True, blank=True, null=True)
    conflict = models.NullBooleanField(db_index=True)

    class Meta:
        unique_together = ("legislator", "vote")
