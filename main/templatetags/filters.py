from django import template
import random
from main.models import *
register = template.Library()

@register.filter()
def rating_class(food):
    return random.choice(["r1","r2","r3","r4","r5"])


@register.filter()
def location_name(location):
    for tag, name in Offering.LOCATION_CHOICES:
        if tag == location:
            return name

@register.filter()
def meal_name(meal):
    for tag, name in Offering.MEAL_CHOICES:
        if tag == meal:
            return name
