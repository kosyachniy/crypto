from time import sleep
from multiprocessing import Process, Manager

def worker(x, i, *args):
    sub_l = Manager().list(x[i])
    sub_l.append(i)
    x[i] = sub_l

def monitor(x):
	print(123)
	while True:
		p=[]
		for i in range(5):
			p.append(Process(target=worker, args=(x, i)))
			p[i].start()
		for i in range(5):
			p[i].join()
		#x.append([1, 0.01, 25, 9, 15, 10])
		sleep(5)
		print(x, p)