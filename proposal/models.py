# -*- coding: utf-8 -*-
from django.db import models


class Proposal(models.Model):    
    proposer = models.ManyToManyField('legislator.Legislator', through='Legislator_Proposal')
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
    legislator = models.ForeignKey('legislator.Legislator', to_field="uid")
    proposal = models.ForeignKey(Proposal)
    priproposer = models.NullBooleanField()


