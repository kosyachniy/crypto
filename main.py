from multiprocessing import Process, Manager
#import monitor, bot
from trade import trade

#p1=Process(target=monitor)
p2=Process(target=trade)
#p3=Process(target=bot)

#p1.start()
p2.start()
#p3.start()