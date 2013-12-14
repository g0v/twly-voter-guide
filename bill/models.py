# -*- coding: utf-8 -*-
from django.db import models


class Bill(models.Model):    
    proposer = models.ManyToManyField('legislator.Legislator', null=True, through='Legislator_Bill')
    billid = models.IntegerField()
    proposalid = models.IntegerField()
    law = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=100,null=True)
    motivation = models.TextField(max_length=500,null=True)
    description = models.TextField(max_length=1000,null=True)
    date = models.DateField(null=True)
    committee = models.CharField(max_length=50,null=True)
    sessionPrd = models.PositiveIntegerField(null=True)
    progress = models.CharField(max_length=50,null=True)
    hits = models.IntegerField(null=True,default=0)
    def __unicode__(self):
        return self.title

    @property
    def sorted_proposer_set(self):
        return self.proposer.all().order_by('legislator_bill__id')

    @property
    def primary_proposer(self):
        return self.proposer.filter(legislator_bill__bill_id=self.id,legislator_bill__priproposer=True)    

class Legislator_Bill(models.Model):    
    legislator = models.ForeignKey('legislator.Legislator', to_field="uid")
    bill = models.ForeignKey(Bill)
    priproposer = models.NullBooleanField()

class BillDetail(models.Model):    
    bill = models.ForeignKey(Bill)
    article = models.CharField(max_length=100,null=True)
    before = models.TextField(max_length=3000,null=True)
    after = models.TextField(max_length=3000,null=True)
    description = models.TextField(max_length=1000,null=True)
    class Meta:
        ordering = ['id'] 
