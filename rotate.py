
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from databaseHandler import dbFile, getCredentials
from sessionHandler import doLogin, checkResponse
import sqlite3

# Time interval in which rotation will happen, in minutes
rotateValue = 60

''' function to rotate ids'''
def rotate():
	db = sqlite3.connect(dbFile)
	cursor = db.cursor()

	# Get random user credentials
	data = getCredentials(cursor)

	# Checking if there was data was not NULL and False
	if data is not False and data is not None:
		# Checking if login can be done using current credentials
		checkLogin = doLogin(cursor, data[1], data[2])
		if checkResponse(checkLogin, 1) is True:
			# Login successful
			now = datetime.now() + timedelta(minutes=rotateValue)
			print("\njob done, Next job in "+now.strftime('%Y-%m-%d %H:%M:%S'))
		else:
			# login was not successful, retry
			rotate()

		# Close databse connection
		db.close()
	else:
		# Retry
		rotate()

''' main function '''
if __name__ == '__main__':
	# Initial Rotate
	rotate()

	# Scheduler configurations
	shed = BlockingScheduler()
	shed.configure(timezone='Asia/Kolkata')
	shed.add_job(rotate, 'interval', minutes=rotateValue)
	#stating scheduler
	shed.start()
	shed.shutdown()
