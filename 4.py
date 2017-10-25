from multiprocessing import Process

from dva import monitor

if __name__ == '__main__':
	p1 = Process(target=monitor)
	p1.start()