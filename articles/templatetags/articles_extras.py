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
