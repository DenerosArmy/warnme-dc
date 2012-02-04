# Create your views here.
from django.http import HttpResponse
import datetime
from main.models import *

def gendb(request):
    """Generate the database"""

    file = open("~/Code4Cal/warnme-dc/menu/data/food")
    foods = file.readlines()
    for each in foods:
	data = each.split(";")
	food = data[0][9:].strip() 
	tags = data[1][10:].strip().split(",")  
	if len(food) == 0:
		continue 
	query = Food.objects.filter(name=food):
	if not query:
		f = Food(name=food) 
		f.save() 
	else:
		f=query[0] 
	if not tags:
		continue 
	
	for tag in tags:
		query = FoodTag.objects.filter(name=tag):
		if not query:
			t = FoodTag(tag) 
			t.save() 
		else:
			 t = query[0] 
		f.tags.add(t) 
		f.save() 

	
		
	
	
	

    html = "<html><body>Database generated successfully</body></html>"
    return HttpResponse(html)
