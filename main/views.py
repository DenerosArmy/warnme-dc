from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
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
    o = Offering.objects.filter(location=location, date=date, meal=meal)
    if len(o) == 0:
        return {}
    else:
        return {"main_foods": o[0].foods.order_by("-rating"),
                "other_foods": []}

def food(request):
    return render_to_response('food.html', RequestContext(request, {}))

def food_profile(request,num):
    return render_to_response('food_pf.html', RequestContext(request,{
                'id': num}))

def user_profile(request,num):
    return render_to_response('user.html', RequestContext(request,{
                'id': num}))
