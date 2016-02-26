# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import JSONField


class Bill(models.Model):
    proposer = models.ManyToManyField('legislator.LegislatorDetail', through='Legislator_Bill')
    uid = models.TextField(primary_key=True)
    ad = models.IntegerField(db_index=True, )
    data = JSONField(null=True)
    for_search = models.TextField(null=True)
    def __unicode__(self):
        return self.uid

class Legislator_Bill(models.Model):
    legislator = models.ForeignKey('legislator.LegislatorDetail', related_name='bills')
    bill = models.ForeignKey(Bill)
    role = models.CharField(max_length=32, db_index=True, )

    class Meta:
        unique_together = ("legislator", "bill")

class Law(models.Model):
    bill = models.ForeignKey(Bill, null=True, related_name='laws')
    uid = models.TextField(primary_key=True)
    ad = models.IntegerField(db_index=True, )
    data = JSONField(null=True)
    def __unicode__(self):
        return self.uid
