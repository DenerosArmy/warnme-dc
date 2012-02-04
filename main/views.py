from django.shortcuts import render_to_response
from main.models import *

def home(request):
    data = {'FH': {'B': { "main_foods": Food.objects.all(),
                          "other_foods": Food.objects.all() }}}
    return render_to_response('home.html', {"data": data})

def food(request):
    return render_to_response('food.html', {})

def food_profile(request,num):
    return render_to_response('food_pf.html', {'id': num})

def user_profile(request,num):
    return render_to_response('user.html', {'id': num})
