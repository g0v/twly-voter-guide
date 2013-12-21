# -*- coding: utf-8 -*-
from django.db import models


class Proposal(models.Model):    
    proposer = models.ManyToManyField('legislator.LegislatorDetail', through='Legislator_Proposal')
    uid = models.CharField(max_length=110, unique=True)
    sitting = models.ForeignKey('sittings.Sittings', to_field="uid")
    proposal_seq = models.CharField(max_length=10)
    content = models.TextField()
    approve = models.IntegerField(blank=True, null=True)
    hits = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.content

    @property
    def sorted_proposer_set(self):
        return self.proposer.all().order_by('legislator_proposal__id')

    @property
    def primary_proposer(self):
        return self.proposer.filter(legislator_proposal__proposal_id=self.uid, legislator_proposal__priproposer=True)
    
class Legislator_Proposal(models.Model):    
    legislator = models.ForeignKey('legislator.LegislatorDetail')
    proposal = models.ForeignKey(Proposal, to_field="uid")
    priproposer = models.NullBooleanField()
