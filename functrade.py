#Торговля по сигналам
from func import *

import pylab #

class YoBit():
	def __init__(self):
		from library.yobit import YoBit as t
		self.trader = t() #оптимизировать
		self.comm = 0.002
		self.min = 0.00011

	#Преобразовать индекс / название валюты для биржи
	def name(self, cur):
		if type(cur) == str:
			return cur.lower() + '_btc'
		else:
			return currencies[cur][1].lower() + '_btc'

	#Баланс валюты
	def info(self, cur='btc'):
		#иногда возникает баг
		#учитывать, что может тратить те деньги, что сейчас на ордере -> ошибка
		try:
			x = self.trader.get_info()['return']['funds_incl_orders'] #funds
		except:
			sleep(5)
			x = self.trader.get_info()['return']['funds_incl_orders']
		return x[cur] if len(cur) else x

	def price(self, cur, buy='buy'):
		if cur == 0 or cur == 'btc':
			return 1 #пока всё покупаем через биткоины

		if cur == 'rur':
			cur = 'btc_rur'
		else:
			cur = self.name(cur)
		res = self.trader.ticker(cur)

		x = 1 if buy in ('sell', 1) else 0
		if cur == 'btc_rur':
			x = (x + 1) % 2
		buy = 'sbeulyl'[x::2]

		#Есть ли эта валюта на бирже и достаточно ли объёма
		if (cur in res) and (res[cur]['vol'] >= 1):
			if cur == 'btc_rur':
				return 1 / res[cur][buy]
			return res[cur][buy]

		#сразу выставлять на продажу по ключевым ценам + снимать если падает оредры и продавать по низкой

		return 0

	#Купить / продать
	def trade(self, cur, count, price, buy):
		name = self.name(cur)
		buys = 'buy' if buy != 1 else 'sell'
		print('bot.send_message(sendid, \'self.trader.trade(\'%s\', \'%s\', %.8f, %.8f)\')' % (name, buys, price, count))
		'''
		try:
			q = self.trader.trade(name, buys, price, count)
			if 'success' not in q:
				return 0
		except:
			return 0
		else:
			return q['return']['order_id']
		'''
		return 1 #
		#синхронизация по исполнению ордеров

	#Умная (быстрая) покупка / продажа
	def real(self, cur, buy='buy', price=0): #sell
		cur = self.name(cur)

		if price == 0:
			#price = self.trader.ticker(cur)[cur]['sell' if buy == 'buy' else 'buy']
			price = self.trader.ticker(cur)[cur][buy] #попробовать продавать по такой цене
		#price = self.trader.ticker(cur)[cur]['last']

		if buy == 'buy':
			total = self.trader.get_info()['return']['funds']['btc']
			delta = total * 0.03
			if delta < self.min:
				delta = self.min
			count = delta / price
		else:
			count = self.trader.get_info()['return']['funds'][cur[:-4]]
			delta = count * price
			if delta < self.min:
				price = self.min / count

		print('%.8f\n%.8f\n%.8f' % (price, count, delta))

		q = self.trader.trade(cur, buy, price, count)
		if q['success']:
			x = q['return']['order_id']
			qm = [0, 0, 0, 0]
			#Ждём 30 секунд исполнения ордера
			for i in range(6):
				print(self.trader.order_info(x)) #
				if self.trader.order_info(x)['return'][str(x)]['status']:
					#Сразу выставляем на продау
					qm[0] = self.trader.trade(cur, 'sell', price * 1.1, count * 0.5)
					qm[1] = self.trader.trade(cur, 'sell', price * 1.15, count * 0.3)
					qm[2] = self.trader.trade(cur, 'sell', price * 1.2, count * 0.1)
					qm[3] = self.trader.trade(cur, 'sell', price * 1.25, count * 0.1)
					return (x, *[i['return']['order_id'] for i in qm])
				else:
					sleep(5)
			return (x, *qm)
		else:
			print('Error!')
			print(q)
			return 0, 0, 0, 0, 0

	def all(self):
		su = 0
		x = self.info('')
		print(x)

		print('Валюта		Количество	Курс		Сумма')
		for i in x:
			pri = self.price(i, 1)
			suma = x[i] * pri
			print(i, '		', str(x[i]) + '	' if type(x[i]) == int else x[i], '	', '%.10f' % pri if type(pri) == float else '%d	' % pri, '	', '%.10f' % suma if suma else 0)
			su += suma

		print('--------------------\n%fɃ\n%f₽' % (su, su * self.trader.ticker('btc_rur')['btc_rur']['buy']))

class Bittrex():
	def __init__(self):
		from library.bittrex import Bittrex as t
		self.trader = t() #оптимизировать
		self.comm = 0.002
		#self.min = 0.00011

	def name(self, cur):
		if type(cur) == str:
			return 'btc-' + cur.lower()
		else:
			return 'btc-' + currencies[cur][1].lower()

	def price(self, cur, buy='buy'):
		cur = cur.lower()
		if cur in ('btc', 0):
			return 1

		cur = self.name(cur)
		x = self.trader.get_ticker(cur)

		buy = 'Bid' if buy in ('sell', 1) else 'Ask'

		if x['success']:
			return x['result'][buy]

		return 0

	def last(self, cur):
		cur = self.name(cur)

		y = []
		for i in self.trader.get_market_history(cur)['result']:
			y.append(i['Price'])

		pylab.plot([i for i in range(1, len(y) + 1)], y)
		pylab.show()
		#pylab.savefig(cur + '.png', format='png', dpi=150)