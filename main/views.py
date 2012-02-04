from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms

import datetime
from math import log10
from main.models import *

def home(request):
    data = {}
    date = datetime.date.today()
    try:
        user_prof = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_prof = None
    except TypeError:
        user_prof = None

    if user_prof != None:
        for location in map(lambda x: x[0], Offering.LOCATION_CHOICES):
            data[location] = {}
            if date.isoweekday() != 6 and date.isoweekday() != 7:
                data[location]['B'] = filter_blacklists(user_prof, date, location, 'B')
            data[location]['L'] = filter_blacklists(user_prof, date, location, 'L')
            data[location]['D'] = filter_blacklists(user_prof, date, location, 'D')
    else:
        for location in map(lambda x: x[0], Offering.LOCATION_CHOICES):
            data[location] = {}
            if date.isoweekday() != 6 and date.isoweekday() != 7:
                data[location]['B'] = sorted_foods(date, location, 'B')
            data[location]['L'] = sorted_foods(date, location, 'L')
            data[location]['D'] = sorted_foods(date, location, 'D')
    return render_to_response('home.html',
                              RequestContext(request,{"data":data}))

def sorted_foods(date, location, meal):
    """Return a dict of main_foods and other_foods for a given offering"""
    o = Offering.objects.filter(location=str(location), date=date, meal=str(meal))
    if len(o) == 0:
        print "returning empty"
        return {}
    else:
        return {"main_foods": o[0].foods.order_by("-rating"),
                "other_foods": []}

def filter_blacklists(user, date, location, meal):
    """Return a dict of main_foods and other_foods for a given offering"""
    offerings = Offering.objects.filter(location=str(location), date=date,
                                        meal=str(meal))
    if len(offerings) == 0: return {}
    offerings = offerings[0].foods.order_by("-rating")
    main_foods, blacklisted_foods = [], []
    for food in offerings:
        blacklisted = False
        for tag in user.blacklisted_tags.all():
            if food in tag.foods.all():
                print str(food), str(tag)
                blacklisted_foods.append(food)
                blacklisted = True
                break
        if not blacklisted: main_foods.append(food)

    return {"main_foods": main_foods,
            "other_foods": blacklisted_foods}

def has_rated(user, food):
    """Returns if a user has voted on a certain food recently."""
    try:
        lastvotetime = UserRating.objects.filter(user=user, food=food).order_by("-id")[0].time
        timediff = datetime.datetime.now() - lastvotetime
        if abs(timediff.days) > 1: return False
        return True
    except IndexError:
        return False

@login_required
def rate(request, food_key, rating):
    """Rate a given food (with key).

    The actual 'value' of the rating is deduced based on the circumstances
    (e.g. whether the user is rating past food already eaten, or new food
    yet to be offered)

    :param rating: 0 means thumbs down, 1 means thumbs up
    """
    try:
        rating = int(rating)
        if rating not in (0, 1):
            return HttpResponse("Error: bad rating key")
        food = Food.objects.get(id=food_key)
        if has_rated(request.user, food): 
            return HttpResponse("You have already voted on this recently. Please try again.")
        votecount = UserRating.objects.filter(user=request.user).count()+0.1
        if votecount < 1.1: votecount = 1.1
        weight = log10(votecount)
        if weight > 1.5: weight = 1.5
        rating = -((-1)**rating)*weight
        u = UserRating(user=request.user,
                       food=food,
                       rating=rating)
        food.add_rating(rating)
    except ObjectDoesNotExist:
        return HttpResponse("Error: Food does not exist")
    except MultipleObjectsReturned:
        assert False
    else:
        u.save()
        return home(request)
        #return HttpResponse("Success")

@login_required
def add_tag(request, tag_key):
    """Add a blacklist tag for the user
    """
    print "adding tag..."
    u_p = UserProfile.objects.get(user=request.user)
    tag = FoodTag.objects.get(id=int(tag_key))
    if tag not in u_p.blacklisted_tags.all():
        u_p.blacklisted_tags.add(tag)
        return HttpResponse("Success")
    else:
        return HttpResponse("Already there")

@login_required
def remove_tag(request, tag_key):
    """Add a blacklist tag for the user
    """
    u_p = UserProfile.objects.get(user=request.user)
    tag = FoodTag.objects.get(id=int(tag_key))
    if tag in u_p.blacklisted_tags.all():
        u_p.blacklisted_tags.remove(tag)
        return HttpResponse("Success")
    else:
        return HttpResponse("Not removed")


def food(request):
    return render_to_response('food.html', RequestContext(request, {}))

def food_profile(request,num):
    return render_to_response('food_pf.html', RequestContext(request,{
                'id': num}))


@login_required
def user_profile(request):
    u_p = UserProfile.objects.get(user=request.user)
    f_t = [ x for x in FoodTag.objects.all() if not x.name.startswith("Vegan") and not x.name.startswith("Vegetarian") ]
    f_t2 = [ (tag, (tag in u_p.blacklisted_tags.all()) ) for tag in f_t ]
    print f_t2
    return render_to_response('user.html',
                              RequestContext(request,{
                "profile": u_p,
                "tags": f_t2}))

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")

    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username');
        password = request.POST.get('password');

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/home/")
                state = "You're successfully logged in!"
            else:
                state = "Your acount is not active, please contact the site admin."
        else:
            state = "Your username and/or password is incorrect."

    return render_to_response('login.html', RequestContext(request,{
                'state':state, 'username':username}))

def logout_user(request):
    if not request.user.is_authenticated():
        state = "You are not logged in"

    logout(request)
    state = "You are now logged out"
    return render_to_response('logout.html', RequestContext(request,{
                    'state':state}))

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login")
    else:
        form = UserCreationForm()
    return render_to_response("register.html", RequestContext(request,{
        'form': form,
    }))

