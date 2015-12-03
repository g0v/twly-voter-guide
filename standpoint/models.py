# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models


class Standpoint(models.Model):
    title = models.CharField(max_length=32, db_index=True)
    vote = models.ForeignKey('vote.Vote', related_name='standpoints', null=True)
    pro = models.IntegerField(default=0)
    class Meta:
        unique_together = ('title', 'vote')

    def __unicode__(self):
        return self.title

class User_Standpoint(models.Model):
    standpoint = models.ForeignKey(Standpoint)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='standpoints')
    class Meta:
        unique_together = ('standpoint', 'user')
