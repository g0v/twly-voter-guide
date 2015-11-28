# -*- coding: utf-8 -*-
import re
import json
from django.core.serializers.json import DjangoJSONEncoder
from django import template
from django.utils.safestring import mark_safe
from legislator.models import LegislatorDetail


register = template.Library()

@register.filter(name='json_lookup')
def json_lookup(value, arg):
    return value.get(arg) if value else None

@register.filter(name='distinct_county')
def distinct_county(value):
    return LegislatorDetail.objects.filter(ad=value).exclude(county='').values_list('county', flat=True).distinct().order_by('county')

@register.filter(name='ad_year')
def ad_year(value, just_start=False):
    term_end_year = {1:1993, 2:1996, 3:1999, 4:2002, 5:2005, 6:2008, 7:2012, 8:2016, 9:2020}
    try:
        value = int(value)
        if just_start:
            return term_end_year.get(value-1, '')
        else:
            return '%s~%s' % (term_end_year.get(value-1, ''), term_end_year.get(value, ''))
    except Exception, e:
        return ''

@register.filter(name='vote_result')
def vote_result(value, arg):
    attribute = {
        'Passed': {
            'td_bgcolor': u'CCFF99',
            'cht': u'通過'
        },
        'Not Passed': {
            'td_bgcolor': u'FF99CC',
            'cht': u'不通過'
        }
    }
    if attribute.get(value):
        return attribute.get(value).get(arg)

@register.filter(name='mod')
def mod(value, arg):
    return value % arg

@register.filter(name='subtract')
def subtract(value, arg):
    try:
        return int(value) - arg
    except:
        return value

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='divide')
def divide(value, arg):
    if arg:
        try:
            return "{0:.2f}".format(100.0 * value / arg)
        except Exception, e:
            print e
    else:
        return 0

@register.filter(name='as_json')
def as_json(data):
    return mark_safe(json.dumps(data, cls=DjangoJSONEncoder))

@register.filter(name='replace')
def replace(value, arg):
    if arg:
        for word in arg.split():
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            value = pattern.sub('<font style="background-color: #FFFF66;">'+word+'</font>', value)
        return value
    else:
        return value
