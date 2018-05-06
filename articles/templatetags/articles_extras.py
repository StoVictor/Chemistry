from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='addstr')
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter(name='substr')
@stringfilter
def substr(arg):
    """return a substring starting with seven liters"""
    return arg.replace('Topic: ', '')

@register.filter(name='substract')
def substract(arg1, arg2):
    "substract arg2 from arg1"
    return arg1-arg2

@register.filter(name='extsubstr')
def extsubstr(arg1, arg2):
    s = ''
    for i in range(0, int(arg2)+1):
        s += arg1[i];
    return s
