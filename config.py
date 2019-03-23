import json
import logging

''' defining variables '''
cyberoamURL = ""
successMsg = "You have successfully logged in"
maxMsg = "You have reached Maximum Login Limit"
tryMsg = "Try again"
oldusr = ''
cfg = ''
prev_login = False

''' opening configuration file '''
try:
	with open('config.json', "r") as file:
		cfg = json.load(file)

# if configuration file do not exist or is corrupted then display error message and create a new configuration file
except:
	print("No config file found. Creating one.")
	try:
		with open('config.json', "rw") as file:
			json.dump({"last_user": "", "last_pass": "", "cur_user": "", "cur_pass": ""}, file, indent=1, ensure_ascii=False)
	except:
		print("Couldn't create config file seems like you don't have enough permission.")

logging.basicConfig()