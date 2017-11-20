from func.trade import *
import numpy as np

cur, limit = 'dash', 20
cur = stock[0].name(cur)

tim = lambda x: x // 60

y = stock[0].trader.trades(cur, limit)[cur]

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

#График
y = [i[1:] for i in al]
x = [i[0] for i in al]

'''
#spread = np.random.rand(2) * 100
center = np.array([0.05, 0.05])
#flier_high = np.random.rand(2) * 100 + 100
#flier_low = np.random.rand(2) * -100
s = np.array(y[0])
print(s)
data = np.concatenate((s, center, s, s), 0)
print(s, center, s, s, sep='\n')
#data = np.concatenate((30, 50, 100, 10), 0)
pylab.boxplot(data, 0, '')
#pylab.plot(x, y)
#pylab.boxplot(al)
#pylab.xticks(range(1, len(x)+1), x)
'''


pylab.boxplot([1,2,0,3,4])



pylab.grid(True)
pylab.show()




