# -*- coding: utf-8 -*-
from django.db import models
from json_field import JSONField


class Vote(models.Model):
    voter = models.ManyToManyField('legislator.Legislator', through='Legislator_Vote')
    content = models.TextField(max_length=1000)
    date = models.DateField(null=True)
    sessionPrd = models.PositiveIntegerField(null=True)
    session = models.CharField(max_length=200)
    hits = models.IntegerField(null=True)
    likes = models.IntegerField(null=True)
    dislikes = models.IntegerField(null=True)
    conflict = models.NullBooleanField()
    results = JSONField(null=True)
    def __unicode__(self):
        return self.content

    def _vote_result(self):
        vote = Legislator_Vote.objects.filter(vote_id=self.id)
        if vote.filter(decision=1).count() > vote.filter(decision=-1).count():
            return False
        else:
            return True
    disapprove = property(_vote_result)

class Legislator_Vote(models.Model):
    legislator = models.ForeignKey('legislator.Legislator')
    vote = models.ForeignKey(Vote)
    decision = models.IntegerField(null=True)
    conflict = models.NullBooleanField()
    class Meta:
        ordering = ['-decision']
