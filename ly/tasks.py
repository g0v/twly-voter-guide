# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from haystack import connections

from vote.models import Vote


@shared_task
def update_vote_index(vote_id):
    connections['default'].get_unified_index().get_index(Vote).update_object(Vote.objects.get(uid=vote_id))
