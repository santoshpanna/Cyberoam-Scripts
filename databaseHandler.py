import sqlite3
import random
import time
from datetime import datetime

dbFile = 'cyberoam.db'
tableExist = False
maxID = None

''' function to check whether table exists '''
def checkTableExists(cursor):
	global tableExist
	if tableExist is False:
		cursor.execute('''SELECT count(*) FROM sqlite_master WHERE type="table" AND name="users"''')
		res = cursor.fetchone()
		if res[0] is 1:
			tableExist = True

	return tableExist

''' function to get max id '''
def getMax(cursor):
	global maxID
	if maxID is None:
		cursor.execute('''SELECT MAX(uid) FROM users''')
		res = cursor.fetchone()
		maxID = res[0]

	return maxID 

''' fucntion to get users details '''
def getCredentials(cursor):
	# Check if table exists from cache variable
	if checkTableExists(cursor) is True:
		# If valid = 1 then user hasn't changed their password and login details are valid
		# Also check that same id is not logged in twice in a single day
		query = '''SELECT * FROM users WHERE uid = ? and valid = ? and lastlogin is not ? limit 1'''
		random.seed(datetime.now())
		uid = [random.randint(1, getMax(cursor)), 1, time.strftime('%Y-%m-%d')]
		cursor.execute(query, uid)
		return cursor.fetchone()
	else:
		# Table doesn't exist return false and deal with in calling function
		print("Table doesn't exist.")
		return False

''' function to insert user '''
def insertUser(cursor, userid, password):
	# Checking if table exists
	
	if checkTableExists(cursor) is False:
		# If table doesn't exist create one
		createTable = '''CREATE TABLE users (uid INTEGER PRIMARY KEY ON CONFLICT ROLLBACK AUTOINCREMENT NOT NULL UNIQUE, userid STRING UNIQUE NOT NULL, password STRING NOT NULL, valid BOOLEAN NOT NULL, lastlogin DATE)'''
		cursor.execute(createTable)
	else :
		# formulating query
		query = '''INSERT INTO {} (uid, userid, password, valid, lastlogin) VALUES (?,?,?,?,?)'''.format("users")
		data = [None, userid, password, 1, None]
		# Trying to insert the userdetails
		try:
			cursor.execute(query, data)
			return True
		# Couldn't insert
		except:
			return False

''' function to update user details with new one '''
def updateUser(cursor, userid, valid):
	if checkTableExists(cursor) is True:
		# If valid = 1 then user hasn't changed their password and login details are valid
		query = '''UPDATE users set valid = ?, lastlogin = ? where uid = ?'''
		
		# If login is valid set valid = 1 and last login = current date
		if valid is 1:
			data = [valid, time.strftime('%Y-%m-%d'), userid]
		# If login is not valid set valid = 0 and last login = NULL
		else:
			data = [valid, time.strftime('%Y-%m-%d'), userid]

		# Try executing the query
		try:
			cursor.execute(query, data)
			return True
		except:
			print("Couldn't update values.")
			return False
	else:
		# Table doesn't exist return false and deal with in calling function
		print("Table doesn't exist.")
		return False