# -*- coding: utf-8 -*-
from haystack import indexes

from .models import Legislator, LegislatorDetail


class LegislatorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    uid = indexes.CharField(model_attr='uid')
    name = indexes.CharField(model_attr='name')
    latest_ad = indexes.IntegerField()

    def get_model(self):
        return Legislator

    def prepare_latest_ad(self, obj):
        return LegislatorDetail.objects.filter(legislator=obj).order_by('-ad').values_list('ad', flat=True)[0]
