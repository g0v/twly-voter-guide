# -*- coding: utf-8 -*-
from haystack import indexes
from .models import Bill


class BillIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    ad = indexes.IntegerField(model_attr='ad')
    uid = indexes.CharField(model_attr='uid')
    abstract = indexes.CharField(model_attr='abstract', null=True)
    last_action_at = indexes.DateField(model_attr='last_action_at', null=True)
    last_action = indexes.CharField(model_attr='last_action', null=True)

    def get_model(self):
        return Bill
