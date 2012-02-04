import sys, os 
sys.path.insert(0, os.path.abspath('..')) 
import settings 
from django.core.management import setup_environ 
setup_environ(settings) 

from main.models import *

file = open("SampleFoodList") 
foods = file.readlines()
for food in foods: 
	t = FoodTag(name=str(food)) 
	t.save() 


