import urllib 
from BeautifulSoup import *
import subprocess
""" Gathers data from dining common website and stores results in text file """ 
BLANK_LENGTH = 10170
skipped = False 
skip_count = 0 
DC = "FOOTHILL"
PATH = "/Users/vaishaal/Code4Cal/warnme-dc/menu/data/{0}".format(DC)
working_file = open(PATH + "/food", "w")
good_file = True
food_name = "dur" 
for i in range(231000, 300000):
		page = urllib.urlopen("http://services.housing.berkeley.edu/FoodPro/dining/static/label.asp?locationNum=06&locationName={0}&dtdate=2%2F3%2F2012&RecNumAndPort={1}".format(DC,i)) 
		data = page.read() 
		if len(data) <= 10170 :
			continue
		soup = BeautifulSoup(data)
		food_name = list(iter(soup.form.div))[0].split(";")[4].rstrip().__str__() 
		food_name += '\n' 
		print(food_name) 
		working_file.write(food_name)
working_file.close() 


