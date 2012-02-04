# Create your views here.
from django.http import HttpResponse
import datetime
from main.models import *

def gendb(request):
    """Generate the database"""

    file = open("/home/nikita/dev/warnme-dc/menu/SampleFoodList")
    foods = file.readlines()
    for food in foods:
        t = Food(name=str(food), rating=0.0)
        t.save()

    html = "<html><body>Database generated successfully</body></html>"
    return HttpResponse(html)
