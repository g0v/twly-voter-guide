# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import JSONField


class Sittings(models.Model):
    uid = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    committee = models.TextField(blank=True, null=True)
    date = models.DateField(db_index=True, )
    ad = models.PositiveIntegerField()
    session = models.PositiveIntegerField()
    links = JSONField(null=True)
    def __unicode__(self):
        return self.name
