from multiprocessing import Process

from func import stock

from dva import monitor

p2 = Process(target=monitor, args=(stock,)) #
p2.start()