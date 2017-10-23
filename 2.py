from multiprocessing import Process, Array

from func import stock

from dva import monitor

if __name__ == '__main__':
	q = Array('stock', stock)

	p1 = Process(target=monitor, args=(q,))
	p1.start()