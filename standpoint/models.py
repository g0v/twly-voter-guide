# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models


class Standpoint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_standpoints', null=True)
    uid = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=32, db_index=True)
    vote = models.ForeignKey('vote.Vote', related_name='standpoints', null=True)
    bill = models.ForeignKey('bill.Bill', related_name='standpoints', null=True)
    pro = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title

class User_Standpoint(models.Model):
    standpoint = models.ForeignKey(Standpoint)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='standpoints')
    create_at = models.DateTimeField(db_index=True, auto_now_add=True, null=True)
    class Meta:
        unique_together = ('user', 'standpoint')
        index_together = ['user', 'standpoint']
