from django.http import HttpResponse
import datetime

def home(request):
    html = "<html><body>This is the home page</body></html>"
    return HttpResponse(html)

def food(request):
    html = "<html><body>This is the list of food</body></html>"
    return HttpResponse(html)

def food_profile(request,num):
    html = "<html><body>This is the information about food with id %s</body></html>" %(num)
    return HttpResponse(html)

def user_profile(request,num):
    html = "<html><body>This is the information about user with id %s</body></html>" %(num)
    return HttpResponse(html)
