from django.utils import simplejson
from django import template
from django.utils.safestring import mark_safe
import re
register = template.Library()

@register.filter(name='mod')
def mod(value, arg):
    return value % arg

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='divide')
def divide(value, arg):
    return "{0:.2f}".format(100.0 * value / arg)

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
