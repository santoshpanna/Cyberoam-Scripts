import argparse

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument('--file', help='enter the filename with extension, default = user.txt', nargs='?', default='user.txt')
argumentParser.add_argument('--batch', help='enter the upper limit for id', nargs='?')
argumentParser.add_argument('--lower', help='enter the lower limit for id, default = 10001', nargs='?', default='10001')
argumentParser.add_argument('--upper', help='enter the upper limit for id', nargs='?')
argumentParser.add_argument('--year', help='enter the year, eg 18 => 2018', nargs='?')
fileArgs = argumentParser.parse_args()

upper = int(fileArgs.upper)+1

with open(fileArgs.file, 'a') as file:
	for rollno in range(int(fileArgs.lower), upper):
		if rollno:
			user="{}{}{}".format(fileArgs.batch, rollno, fileArgs.year)
		file.write(str(user)+'\n')