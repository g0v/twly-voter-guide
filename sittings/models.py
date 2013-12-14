# -*- coding: utf-8 -*-
from django.db import models

class Sittings(models.Model):
    uid = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=200)
    committee = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField()
    ad = models.IntegerField()
    session = models.IntegerField()
    def __unicode__(self):
        return self.name
