import urllib.parse
import urllib.request
import ssl
import config
from databaseHandler import updateUser
import time
import json

cyberoamURL = ""
successMsg = "You have successfully logged in"
maxMsg = "You have reached Maximum Login Limit"
tryMsg = "Try again"

''' function to login '''
def login(userid, password):
	dataToSend = urllib.parse.urlencode({'mode': '191','isAccessDenied': '', 'url': '', 'username': userid, 'password': password, 'saveinfo': ''}).encode("utf-8")
	gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	try:
		postRequest = urllib.request.urlopen(cyberoamURL, dataToSend, context=gcontext)
		responseData = postRequest.read().decode()
		return responseData

	except urllib.error.URLError:
		# If timeout error wait for 5 minutes
		time.sleep(300)
		print("Timeout error waiting 5 minutes")
		postRequest = urllib.request.urlopen(cyberoamURL, dataToSend, context=gcontext)
		responseData = postRequest.read().decode()
		return responseData

''' function to logout '''
def logout(userid, password):
	dataToSend = urllib.parse.urlencode({'mode': '193','isAccessDenied': '', 'url': '', 'username': userid, 'password': password, 'saveinfo': ''}).encode("utf-8")
	gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	postRequest = urllibd.request.urlopen(cyberoamURL, dataToSend, context=gcontext)

''' function used when checking for password (bruteforce) '''
def checkResponse(res, type):
	if successMsg in res:
		return True
	# type = 0, checking while bruteforce
	# type > 0, checking for login 
	if type == 0:
		if maxMsg in res:
			return True
	else:
		return False

''' function used when doing login from db file '''
def doLogin(cursor, userid, password):
	'''
	# Logout from previous account
	if prevLogin == True:
		logout(config.cfg['cur_user'], config.cfg['cur_pass'])
	'''
	# Check if login is successful
	res = login(userid, password)

	# Login is successful
	if successMsg in res:
		# Update configuration file with new values
		with open('config.json', "w") as file:
			json.dump({"last_user": config.cfg['cur_user'], "last_pass": config.cfg['cur_pass'], "cur_user": config.userid, "cur_pass": config.password}, file, indent=1, ensure_ascii=False)
		#update the database
		updateUser(cursor, userid, 1)
		return True
	else:
		#update the database
		updateUser(cursor, userid, 0)
		return False