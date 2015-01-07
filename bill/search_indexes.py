# -*- coding: utf-8 -*-
from haystack import indexes

from .models import Bill, ttsMotions


class BillIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    ad = indexes.IntegerField(model_attr='ad')
    uid = indexes.CharField(model_attr='uid')
    abstract = indexes.CharField(model_attr='abstract', null=True)
    proposed_by = indexes.CharField(model_attr='proposed_by', null=True)
    last_action_at = indexes.DateField(model_attr='last_action_at', null=True)
    last_action = indexes.CharField(model_attr='last_action', null=True)
    rejected_times = indexes.IntegerField()
    progress_history = indexes.MultiValueField()

    def get_model(self):
        return Bill

    def prepare_rejected_times(self, obj):
        return ttsMotions.objects.filter(bill=obj, progress='退回程序').count()

    def prepare_progress_history(self, obj):
        return [(x.progress, x.date, ) for x in ttsMotions.objects.filter(bill=obj).order_by('-date')]
