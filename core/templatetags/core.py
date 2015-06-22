from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def short_timesince(value):
    return timesince(value).split(',')[0]
