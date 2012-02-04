import datetime 
import urllib 
from BeautifulSoup import * 
from main.models import *
from django.http import HttpResponse

Date = datetime.date.today() 
KEYWORDS = ["Breakfast", "Lunch", "Dinner", "Brunch"] 	
def genmenu(request = None): 
		menu = urllib.urlopen("http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp").read() 
		soup = BeautifulSoup(menu) 
		search = soup.findAll(["a", "b"]) 
		meals = {i:[] for i in range (0,12)} 
		mealtags = {0:"CR;B", 1:"C3;B", 2:"FH;B", 3:"CKC;B", 4:"CR;L", 5:"C3;L", 6:"FH;L",7:"CKC;L", 8:"CR;D", 9:"C3;D",10:"FH;D",11:"CKC;D"} 
		Foods = [each.getText().__str__() for each in search] 
		Foods = Foods[12:-7]
		colortags = {"800040":"Vegan","000A0":"Vegetarian w/Dairy or Eggs","008000":"Vegetarian"}
		food_to_tags = {} 
		for i in colortags.values(): 
			t, boolean = FoodTag.objects.get_or_create(name=str(i)) 
			t.save() 
		for i in list(soup.findAll("font")): 
			i = str(i)
			if i[6:11] == "color":
				if i[14:20] in colortags:
					food_to_tags[i[22:-7]] = colortags[i[14:20]] 
			

		for i in range(Foods.count("Nutritive Analysis")):  
			Foods.remove("Nutritive Analysis") 
		print(Foods) 
		MealCount = -1  
		FoodStart = False
		for each in Foods:

			if each in KEYWORDS:
				FoodStart = False
				MealCount += 1
			else:
				FoodStart = True 
			
			CurrMeal = meals[MealCount] 
			if FoodStart:
				CurrMeal.append(each) 

		for number in meals:
			mealdata = mealtags[number]
			print mealdata
			mealdata = mealdata.split(";") 

			location = mealdata[0] 
			meal = mealdata[1] 
			O = Offering(meal=meal,location = location, date=Date ) 
			O.save()
			for food in meals[number]:
				f, boolean = Food.objects.get_or_create(name=food,defaults={"rating":0.0} )
				try:
					f.tags.add(FoodTag.objects.get(name=food_to_tags[food]))
					f.save()
				except:
					pass
				O.foods.add(f) 
			O.save()
    
		html = "<html><body>Database generated successfully</body></html>"
		return HttpResponse(html)
