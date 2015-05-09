# -*- coding: utf-8 -*-
from django.db.models import Count

from haystack import indexes

from .models import Vote
from standpoint.models import Standpoint


class VoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    uid = indexes.CharField(model_attr='uid')
    category = indexes.CharField(default=None, model_attr='category')
    content = indexes.CharField(model_attr='content')
    conflict = indexes.BooleanField(default=None, model_attr='conflict')
    ad = indexes.IntegerField(model_attr='sitting__ad')
    date = indexes.DateField(model_attr='sitting__date')
    vote_seq = indexes.CharField(model_attr='vote_seq')
    result = indexes.CharField(model_attr='result')
    results = indexes.CharField(model_attr='results')
    tags = indexes.MultiValueField()

    def get_model(self):
        return Vote

    def prepare_tags(self, obj):
        return [
                   (x.title, x.votes, )
                   for x in
                   Standpoint.objects.filter(vote=obj)\
                                     .annotate(votes=Count('user_standpoint__id'))\
                                     .order_by('-votes')
               ]
