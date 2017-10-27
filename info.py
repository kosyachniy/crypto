from func.main import *

#сделать регулярным по расписанию celery
while True:
	if gmtime().tm_hour == 20 + utc:
		for j in range(len(stock)):
			send(stock[j].all())
	sleep(3600)