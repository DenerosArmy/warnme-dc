from GV import * 
def text(number, message):
	voicei= voice.Voice()
	voicei.login("vaishaal@berkeley.edu", "warnmedc") 
	sending = "Hello this is a friendly warning from WarnMeDc!\n" 
	sending += message 
	voicei.send_sms(number, sending) 


	

