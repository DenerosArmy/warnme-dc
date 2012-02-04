from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import datetime
from math import log10
from main.models import *

def home(request):
    data = {}

    date = datetime.date.today()
    for location in map(lambda x: x[0], Offering.LOCATION_CHOICES):
        data[location] = {}
        if date.isoweekday() != 6 and date.isoweekday() != 7:
            data[location]['B'] = sorted_foods(date, location, 'B')

        data[location]['L'] = sorted_foods(date, location, 'L')
        data[location]['D'] = sorted_foods(date, location, 'D')

    return render_to_response('home.html', RequestContext(request,{
                "data": data}))

def sorted_foods(date, location, meal):
    """Return a dict of main_foods and other_foods for a given offering"""
    o = Offering.objects.filter(location=str(location), date=date, meal=str(meal))
    if len(o) == 0:
        print "returning empty"
        return {}
    else:
        return {"main_foods": o[0].foods.order_by("-rating"),
                "other_foods": []}

def rate(request, food_key, rating):
    """Rate a given food (with key).

    The actual 'value' of the rating is deduced based on the circumstances
    (e.g. whether the user is rating past food already eaten, or new food
    yet to be offered)

    :param rating: 0 means thumbs down, 1 means thumbs up
    """
    try:
        rating = int(rating)
        if rating not in (0, 1): return HttpResponse("Error: bad rating key")
        votecount = UserRating.objects.filter(user=request.user).count()+0.1
        if votecount < 1.1: votecount = 1.1
        weight = log10(votecount)
        if weight > 1.5: weight = 1.5
        rating = ((-1)**rating)*weight
        u = UserRating(user=request.user,
                       food=food,
                       rating=rating)

    except ObjectDoesNotExist:
        return HttpResponse("Error: Food does not exist")
    except MultipleObjectsReturned:
        assert False
    else:
        u.save()
        return HttpResponse("Success")

def food(request):
    return render_to_response('food.html', RequestContext(request, {}))

def food_profile(request,num):
    return render_to_response('food_pf.html', RequestContext(request,{
                'id': num}))

def user_profile(request,num):
    return render_to_response('user.html', RequestContext(request,{
                'id': num}))


