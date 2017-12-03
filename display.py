from func.trade import *
import numpy as np
from time import mktime, strptime


cur, limit = 'dash', 20
cur = stock[0].name(cur)
y = stock[0].trader.trades(cur, limit)[cur]
y = [[i['timestamp'] // 60, i['price']] for i in y]

'''
cur = 'dash'
cur = stock[1].name(cur)
y = stock[1].trader.get_market_history('btc-ltc')['result']
y = [[mktime(strptime(i['TimeStamp'].split('.')[0], '%Y-%m-%dT%H:%M:%S')) // 60, i['Price']] for i in y]
'''

#Разбиение на минуты
al = []
real_min = 0
real_max = 0
real_open = 0
real_last = 0

mi = y[-1][0]

for i in y[::-1]:
	mo = i[0]
	if mo > mi:
		al.append([mo, real_min, real_open, real_last, real_max])
		real_open = 0
		mi = mo

	if real_open:
		if i[1] < real_min:
			real_min = i[1]
		elif i[1] > real_max:
			real_max = i[1]
		real_last = i[1]
	else:
		real_min = i[1]
		real_max = i[1]
		real_last = i[1]
		real_open = i[1]

al = al[1:][-20:] #первый - не полный, последний - не вносится

#График

y = [i[1:] for i in al]
x = [int(i[0]%60) for i in al]

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

#print(y)
mi = min([min(i) for i in y])
ma = max([max(i) for i in y])

y = y + [[mi,mi,mi,mi],[mi,mi,mi,mi]] #[[mi,mi,mi*1.03,mi*1.03], [mi*1.03,mi*1.03,mi*1.05,mi*1.05]]
x = x + [x[-1]+5, x[-1]+10] #[int((x[-1]+5)%60), int((x[-1]+10)%60)]

pylab.boxplot(y, positions=x) #[i for i in range(1, len(y)+4)]

pylab.annotate(u'Up',
                xy=(x[-3], y[-3][3]),
                xytext = (x[-1], ma+), #y[-3][3]*1.05
                arrowprops = {'arrowstyle': '<|-'}
                )

pylab.grid(True)
pylab.show()




