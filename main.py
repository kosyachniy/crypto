from multiprocessing import Process, Manager
from telegram import telegram
from monitor import monitor

x = Manager().dict()
x = [[1, 0.01, 25, 9, 15, 10]] #['trade'] = 12 #[[1, 2, 3, 4, 5], [1, 2, 3, 4, 6]]

p1 = Process(target=telegram, args=(x,))
p2 = Process(target=monitor, args=(x,))

p1.start()
#p2.start()