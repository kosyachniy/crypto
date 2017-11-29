from func.main import *

#сделать регулярным по расписанию celery
if __name__ == '__main__':
	while True:
		if gmtime().tm_hour - utc in (6, 12, 20):
			for j in range(len(stock)):
				send(stock[j].all())
		sleep(3600)