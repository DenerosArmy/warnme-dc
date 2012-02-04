from texting import * 
date = dateTime.date.today() 
def genwarn(request): 	

	def warn_check(user):
		location = user.default_location
		filteredLunch = filter_blacklist(user,date,location, "L" ) 
		filteredDinner = filter_blacklist(user,date,location, "D") 
		warn_message = "" 
		if len(filteredLunch['main_foods']) < len(filteredLunch['other_foods']):	    	
			warn_message += generate_warn_message(user,"L",filteredLunch) + " \n  " 
		if len(filteredDinner['main_foods'] < len(filteredDinner['other_foods']): 
			warn_message += generate_warn_messafe(user,"D",filteredDinner) 
		if len(warn_message) >= 0: 
			text(user.number, warn_message) 
		
	def generate_warn_message(user,meal,data):
		percentage = float(len(filteredLunch['other_foods']))/((len(filteredLunch['main_foods'] + len(filteredLunch['other_foods'])))) * 100 
		average = sum(filteredLunch['main_foods'])/len(filteredLunch['main_foods']) 
		message = "{0} percent of todays {1} seems to be on your blacklist. The rest of the food has an average rating of {2}. Please making according plans." 
	
		for u in user.profiles.objects.all(): 
			warn(u)

