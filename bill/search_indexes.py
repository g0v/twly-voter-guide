# -*- coding: utf-8 -*-
from haystack import indexes

from .models import Bill


class BillIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    ad = indexes.IntegerField(model_attr='ad')
    uid = indexes.CharField(model_attr='uid')

    def get_model(self):
        return Bill
