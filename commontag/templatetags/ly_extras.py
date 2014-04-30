# -*- coding: utf-8 -*-
import re
from django.utils import simplejson
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='personal_property_summary')
def personal_property_summary(value, arg):
    attribute = {
        'antique': {
            'after_title': u'共',
            'count_unit': u'總',
            'remark': False,
            'cht': u'具有相當價值之財產'
        },
        'otherbonds': {
            'after_title': u'總額',
            'count_unit': u'筆',
            'after_unit': u'約',
            'zhutil_unit': u'price',
            'total_unit': u'元',
            'remark': False,
            'cht': u'其他有價證券'
        },
        'fund': {
            'after_title': u'總額',
            'count_unit': u'筆',
            'after_unit': u'約',
            'zhutil_unit': u'price',
            'total_unit': u'元',
            'remark': False,
            'cht': u'基金'
        },
        'bonds': {
            'after_title': u'總額',
            'count_unit': u'筆',
            'after_unit': u'約',
            'zhutil_unit': u'price',
            'total_unit': u'元',
            'remark': False,
            'cht': u'債券'
        },
        'stock': {
            'after_title': u'總額',
            'count_unit': u'筆',
            'after_unit': u'約',
            'zhutil_unit': u'price',
            'total_unit': u'元',
            'remark': False,
            'cht': u'股票'
        },
        'land': {
            'after_title': u'持有總面積',
            'count_unit': u'筆',
            'after_unit': u'約',
            'zhutil_unit': u'price',
            'total_unit': u'平方公尺',
            'remark': True,
            'cht': u'土地'
        },
        'building': {
            'after_title': u'持有總面積',
            'count_unit': u'筆',
            'after_unit': u'約',
            'zhutil_unit': u'area',
            'total_unit': u'平方公尺',
            'remark': True,
            'cht': u'建物'
        },
        'car': {
            'after_title': u'',
            'count_unit': u'輛',
            'after_unit': u'總汽缸容量約',
            'zhutil_unit': u'area',
            'total_unit': u' cc',
            'remark': False,
            'cht': u'汽車'
        },
        'cash': {
            'after_title': u'總額',
            'count_unit': u'筆',
            'after_unit': u'約',
            'zhutil_unit': u'price',
            'total_unit': u'元',
            'remark': False,
            'cht': u'現金'
        },
        'deposit': {
            'after_title': u'總額',
            'count_unit': u'筆',
            'after_unit': u'約',
            'zhutil_unit': u'price',
            'total_unit': u'元',
            'remark': False,
            'cht': u'存款'
        }
    }
    return attribute.get(value).get(arg)

@register.filter(name='mod')
def mod(value, arg):
    return value % arg

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='multiply')
def subtract(value, arg):
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
    return mark_safe(simplejson.dumps(data))

@register.filter(name='replace')
def replace(value, arg):
    if arg:
        for word in arg.split():
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            value = pattern.sub('<font style="background-color: #FFFF66;">'+word+'</font>', value)
        return value
    else:
        return value
