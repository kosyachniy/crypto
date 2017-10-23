from multiprocessing import Process, Queue

from dva import monitor

if __name__ == '__main__':
	q = Queue()

	p1 = Process(target=monitor, args=(q,))
	p1.start()

from func import stock

while True:
	print(exec(q.get()))