from func.trade import *
from datetime import *

cur, limit = 'dash', 5
cur = stock[0].name(cur)

tim = lambda x: x // 60 #datetime.fromtimestamp(x).strftime('%M')

y = stock[0].trader.trades(cur, limit)[cur] #[i['price'] for i in ]

#Разбиение на минуты
al = []
real_min = 0
real_max = 0
real_open = 0
real_last = 0

mi = tim(y[-1]['timestamp'])

for i in y[::-1]:
	mo = tim(i['timestamp'])
	if mo > mi:
		al.append([mo, real_min, real_open, real_last, real_max])
		real_open = 0
		mi = mo

	if real_open:
		if i['price'] < real_min:
			real_min = i['price']
		elif i['price'] > real_max:
			real_max = i['price']
		real_last = i['price']
	else:
		real_min = i['price']
		real_max = i['price']
		real_last = i['price']
		real_open = i['price']

al = al[1:] #первый - не полный, последний - не вносится
#print(al)

'''
y = stock[0].trader.depth(cur, limit)
print(y)
'''

#График
y = [i[1] for i in al]
x = [i[0] for i in al]

pylab.plot(x, y) #[i for i in range(1, len(y) + 1)]
pylab.grid(True)
pylab.show()