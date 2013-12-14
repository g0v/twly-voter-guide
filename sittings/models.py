# -*- coding: utf-8 -*-
from django.db import models

class Sittings(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    committee = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField()
    ad = models.IntegerField()
    session = models.IntegerField()
    def __unicode__(self):
        return self.name
