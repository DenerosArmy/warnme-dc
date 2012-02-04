# Create your views here.
from django.http import HttpResponse
import datetime
from main.models import *
from DailyFoodGen import genmenu

def gendb(request):
    """Generate the database"""

    file = open("/home/nikita/dev/warnme-dc/menu/data/food")
    foods = file.readlines()
    for i, each in enumerate(foods):
        print "Reached food # {}: {}".format(i, each)

	data = each.split(";")
	food = data[0][9:].strip() 
	tags = [ x.strip() for x in data[1][11:].split(",") ]
	if len(food) == 0:
		continue

        f, created = Food.objects.get_or_create(name=food,
                                                   defaults={"rating":0.0})

	if not tags:
		continue 

	for tag in tags:
		if tag == "":
                    continue

		t, created = FoodTag.objects.get_or_create(name=tag)
		f.tags.add(t) 
	f.save() 


    html = "<html><body>Database generated successfully</body></html>"
    return HttpResponse(html)
