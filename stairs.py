from func.trade import stock, bar
from time import sleep

exc = 1
cur = 'usdt-btc'

def buy():
	y = stock[exc].last(cur)

	m5 = bar(y, 5, 1)
	m1 = bar(y, 1, 1)

	#m5 = m5[list(m5)[0]]
	#m1 = m1[list(m1)[0]]

	m5 = [m5[i] for i in m5]
	m1 = [m1[i] for i in m1]

	if m5[0][-1] >= m5[0][0] and m1[0][-1] > m1[0][0]:
		return m1[0][-1]
	return 0

def sell():
	return stock[exc].price(cur, 'buy')

while True:
	price = buy()

	if price:
		print('In %.8f' % stock[exc].price(cur, 'buy'))

		sleep(60)
		tim = 1
		t = sell()

		while t > price:
			price = t
			sleep(60)
			tim += 1
			t = sell()

		print('Out %.8f (%d min)' % (stock[exc].price(cur, 'sell'), tim))