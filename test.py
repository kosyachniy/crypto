from celery.decorators import periodic_task
from celery.task.schedules import crontab
import time, datetime

@periodic_task(run_every=datetime.timedelta(minutes=1)) #periodic_task(run_every=crontab(minute=25))
def write():
	print(123)

while True:
	write()
	time.sleep(5)