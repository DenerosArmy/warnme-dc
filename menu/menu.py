import urllib 
from BeautifulSoup import *
import subprocess
import sys

def menu_scrape(x,y,foodn): 
	""" Gathers data from dining common website and stores results in text file """ 
	BLANK_LENGTH = 10170
	skipped = False 
	skip_count = 0
	DC = "Foothill" 
	PATH = "/Users/vaishaal/Code4Cal/warnme-dc/menu/data/{0}".format(DC)
	good_file = True
	food_name = "dur" 
	for i in range(x, y):
		working_file = open(PATH + "/food{0}".format(foodn), "w")
		page = urllib.urlopen("http://services.housing.berkeley.edu/FoodPro/dining/static/label.asp?locationNum=06&locationName={0}&dtdate=2%2F3%2F2012&RecNumAndPort={1}".format(DC,i)) 
		data = page.read() 
		if len(data) <= 10170 :
			continue
		soup = BeautifulSoup(data)
		food_name = "FoodName:" + list(iter(soup.form.div))[0].split(";")[4].rstrip().__str__() 
		food_name += "   "
		allergens = "Allergens:" + ((list(list(soup.body)[-6])[-4].getText()).split(";"))[-1].__str__()
		print(food_name + "    " + allergens) 
		working_file.write(food_name)
		working_file.close() 

x = int(sys.argv[1])
y = int(sys.argv[2]) 
z = sys.argv[3] 
menu_scrape(x,y,z) 
