# -*- coding: utf-8 -*-
from haystack import indexes
from .models import Keyword


class KeywordIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content = indexes.CharField(model_attr='content')
    category = indexes.IntegerField(model_attr='category')
    hits = indexes.IntegerField(model_attr='hits')

    def get_model(self):
        return Keyword
