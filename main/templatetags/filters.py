from django import template
from main.models import *
register = template.Library()

@register.filter()
def rating_class(food):
    if food.rating > 0.5:
        return "r5"
    elif food.rating > 0.3:
        return "r4"
    elif food.rating > 0.1:
        return "r3"
    elif food.rating > -0.2:
        return "r2"
    else:
        return "r1"


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

@register.filter()
def get_rating(food):
    votecount = UserRating.objects.filter(food=food).count()
    if votecount == 0: return 0
    return (food.rating)/votecount
