# -*- coding: utf-8 -*-
from django.db import models
from json_field import JSONField

class Sittings(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    committee = models.TextField(blank=True, null=True)
    date = models.DateField()
    ad = models.IntegerField()
    session = models.IntegerField()
    links = JSONField(null=True)
    def __unicode__(self):
        return self.name
