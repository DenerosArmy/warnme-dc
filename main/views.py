from django.shortcuts import render_to_response

def home(request):
    return render_to_response('home.html', {})

def food(request):
    return render_to_response('food.html', {})

def food_profile(request,num):
    return render_to_response('food_pf.html', {'id': num})

def user_profile(request,num):
    return render_to_response('user.html', {'id': num})
