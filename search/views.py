# -*- coding: utf-8 -*-
from search.models import Keyword


def keyword_list(category):
    # 1: proposal, 2: vote, 3: bill
    return list(Keyword.objects.filter(category=category,valid=True).order_by('-hits').values_list('content', flat=True))
