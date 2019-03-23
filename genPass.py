import argparse
import calendar

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument('--file', help='enter the filename with extension, default = pass.txt', nargs='?', default='pass.txt')
argumentParser.add_argument('--lower', help='enter the lower limit for year', nargs='?')
argumentParser.add_argument('--upper', help='enter the upper limit for year', nargs='?')
fileArgs = argumentParser.parse_args()

date_lower = 1

upper = int(fileArgs.upper)+1

with open(fileArgs.file, 'a') as file:
	for year in range(int(fileArgs.lower), upper):
		for month in range(1,13):
			# Getting the last date of the month
			date_upper = calendar.monthrange(int(year), int(month))
			year = str(year)
			for date in range(1, int(date_upper[1])):
				if date < 10:
					dob="0{}{}{}{}".format(date, month, year[2], year[3])
				if month < 10:
					dob="{}0{}{}{}".format(date, month, year[2], year[3])
				elif date < 10 and month < 10:
					dob="0{}0{}{}{}".format(date, month, year[2], year[3])
				else:
					dob="{}{}{}{}".format(date, month, year[2], year[3])
				file.write(str(dob)+'\n')