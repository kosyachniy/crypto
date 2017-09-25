from multiprocessing import Process, Manager
#from telegram import telegram
from monitor import monitor

x = Manager().list()

#p1 = Process(target=telegram, args=(x,))
p2 = Process(target=monitor, args=(x,))

#p1.start()
p2.start()