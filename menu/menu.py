import urllib 
from BeautifulSoup import *
import subprocess
import sys

def menu_scrape(x,y,foodn): 
	""" Gathers data from dining common website and stores results in text file 

	:param int x: lower bound of searching port 
	:param int y: upper bound of searching port 
	:param string foodn: an integer string that identifies a particular output file 

	"""
	BLANK_LENGTH = 10170
	skipped = False 
	skip_count = 0
	PATH = "/Users/vaishaal/Code4Cal/warnme-dc/menu/data/"
	good_file = True
	food_name = "dur" 
	working_file = open(PATH + "/food{0}".format(foodn), "w")
	for i in range(x, y):
		page = urllib.urlopen("http://services.housing.berkeley.edu/FoodPro/dining/static/label.asp?locationNum=06&locationName=FOOTHILL&dtdate=2%2F3%2F2012&RecNumAndPort={0}".format(i)) 
		data = page.read() 
		if len(data) <= 10170 :
			continue
		soup = BeautifulSoup(data)
		food_name = "FoodName:" + list(iter(soup.form.div))[0].split(";")[4].rstrip().__str__() 
		food_name += "   "
		allergens = "Allergens:" + ((list(list(soup.body)[-6])[-4].getText()).split(";"))[-1].__str__()
		text = (food_name + " ; " + allergens + "\n") 
		working_file.write(text) 
x = int(sys.argv[1])
y = int(sys.argv[2]) 
z = sys.argv[3] 
menu_scrape(x,y,z) 
