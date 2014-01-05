# -*- coding: utf-8 -*-
from django.db import models
from json_field import JSONField


class Vote(models.Model):
    voter = models.ManyToManyField('legislator.LegislatorDetail', through='Legislator_Vote')
    uid = models.CharField(max_length=110, unique=True)
    sitting = models.ForeignKey('sittings.Sittings', to_field="uid", related_name='votes')
    vote_seq = models.CharField(max_length=10)
    content = models.TextField()
    hits = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    conflict = models.NullBooleanField()
    results = JSONField(null=True)
    def __unicode__(self):
        return self.content

    def _vote_result(self):
        return self.results.get('agree') <= self.results.get('disagree')
    disapprove = property(_vote_result)

class Legislator_Vote(models.Model):
    legislator = models.ForeignKey('legislator.LegislatorDetail', related_name='votes')
    vote = models.ForeignKey(Vote, to_field="uid")
    decision = models.IntegerField(blank=True, null=True)
    conflict = models.NullBooleanField()
    class Meta:
        ordering = ['-decision']
