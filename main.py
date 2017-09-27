from multiprocessing import Process, Manager
from monitor import monitor
from trade import trade
from bot import bots

p1=Process(target=monitor)
p2=Process(target=trade)
p3=Process(target=bots)

p1.start()
p2.start()
p3.start()