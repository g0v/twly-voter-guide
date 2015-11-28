# -*- coding: utf-8 -*-
from haystack import indexes

from .models import Terms


class CandidatesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    ad = indexes.IntegerField(model_attr='ad')
    county = indexes.CharField(model_attr='county')
    constituency = indexes.CharField(model_attr='constituency')

    def get_model(self):
        return Terms

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(ad=9)
