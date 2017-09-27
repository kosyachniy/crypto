from multiprocessing import Process, Manager
import monitor, bot

p1=Process(target=monitor)
p2=Process(target=bot)

p1.start()
p2.start()