from func.trade import stock, bar
from time import sleep

exc = 1
cur = 'usdt-btc'
deposit_usd = 100
commission = 0.0025

def buy():
	y = stock[exc].last(cur)

	m5 = bar(y, 5, 1)
	m1 = bar(y, 1, 1) #2)

	#m5 = m5[list(m5)[0]]
	#m1 = m1[list(m1)[0]]

	m5 = [m5[i] for i in m5]
	m1 = [m1[i] for i in m1]

	if m5[0][-1] >= m5[0][0] and m1[0][-1] > m1[0][0]: # and m1[1][-1] > m1[1][0]:
		return m1[-1][-1]
	return 0

def sell():
	return stock[1].trader.get_ticker(cur)['result']['Last'] #stock[exc].price(cur, 'buy')

while True:
	price = buy()

	if price:
		bb = stock[exc].price(cur, 'buy')
		deposit_btc = deposit_usd / bb * (1 - commission)
		print('In %.8f' % bb)

		sleep(60)
		tim = 1
		t = sell()

		while t >= price:
			price = t
			sleep(60)
			tim += 1
			t = sell()

		if not buy():
			ss = stock[exc].price(cur, 'sell')
			deposit_usd = deposit_btc * ss * (1 - commission)
			print('Out %.8f (%d min)\n%.2f$ (%.4f%%)\n--------------------' % (ss, tim, deposit_usd, deposit_usd / 100 - 1))