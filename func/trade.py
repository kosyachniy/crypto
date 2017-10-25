#Торговля по сигналам
from func.data import *

'''
from celery.decorators import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery import Task
'''

ru = lambda: float(requests.get('https://blockchain.info/tobtc?currency=RUB&value=1000').text) / 1000

import pylab #

class YoBit():
	def __init__(self):
		from func.library.yobit import YoBit as t
		self.trader = t() #оптимизировать
		self.comm = 0.002
		self.min = 0.00011
		self.per = 0.03

	#Преобразовать индекс / название валюты для биржи
	def name(self, cur):
		if type(cur) == str and '_' in cur:
			return cur
		if type(cur) == int:
			cur = currencies[cur][1]
		cur = cur.lower()
		if cur == 'btc':
			return 0
		elif cur == 'rur':
			return 'btc_rur'
		return cur + '_btc'

	def buys(self, buy='buy', dop=0):
		x = 0 if buy in ('sell', 1) else 1
		return 'sbeulyl'[(x + dop) % 2::2]

	#Перевод в рубли
	def ru(self):
		return 1 / self.trader.ticker('btc_rur')['btc_rur']['buy']

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

	#Курс
	def price(self, cur, buy='buy'):
		cur = self.name(cur)
		if not cur:
			return 1

		res = self.trader.ticker(cur)
		buy = self.buys(buy, 1 if cur != 'btc_rur' else 0)

		#Есть ли эта валюта на бирже
		if cur in res: # and (res[cur]['vol'] >= 1) #и достаточно ли объёма
			if cur == 'btc_rur':
				return 1 / res[cur][buy]
			return res[cur][buy]

		return 0

	#Купить / продать
	def trade(self, cur, count=0, price=0, buy='buy'):
		if not price: price = self.price(cur, buy)
		name = self.name(cur)
		if not count: count = self.info() * self.per / price

		buy = self.buys(buy, 0 if cur != 'btc_rur' else 1)
		print('self.trader.trade(\'%s\', \'%s\', %.8f, %.8f)' % (name, buy, price, count))

		try:
			q = self.trader.trade(name, buy, price, count)
			#print(q)
			if 'success' not in q:
				return 0
		except:
			return 0
		else:
			try:
				return q['return']['order_id']
			except:
				return 0

	#Закрыт ли ордер?
	def order(self, id):
		try:
			if self.trader.order_info(id)['return'][str(id)]['status'] != 0:
				return True
		except:
			pass
		return False

	def cancel(self, id):
		self.trader.cancel_order(id)

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
		from func.library.bittrex import Bittrex as t
		self.trader = t() #оптимизировать
		self.comm = 0.002
		self.min = 0.001 #0.0005 #чтобы потом можно было на loss продать
		self.per = 0.03

	def name(self, cur):
		if type(cur) == str and '-' in cur:
			return cur
		if type(cur) == int:
			cur = currencies[cur][1]
		cur = cur.lower()
		if cur == 'btc':
			return 0
		return 'btc-' + cur

	def buys(self, buy='buy', dop=0):
		x = 0 if buy in ('sell', 1) else 1
		return 'ABsikd'[(x + dop) % 2::2]
	
	def info(self, name='btc'):
		name = name.lower()
		for i in self.trader.get_balances()['result']:
			if i['Currency'].lower() == name:
				return i['Available']

	def ru(self):
		return ru()

	def price(self, cur, buy='buy'):
		if type(cur) == str:
			cur = cur.lower()
		if cur in ('btc', 0):
			return 1

		cur = self.name(cur)
		x = self.trader.get_ticker(cur)
		buy = self.buys(buy, 1)
		if x['success']:
			return x['result'][buy]

		return 0

	def trade(self, cur, count=0, price=0, buy='buy'):
		if not price: price = self.price(cur, buy)
		name = self.name(cur)
		if not count: count = self.info(name.replace('btc-', '')) if buy in ('sell', 1) else self.info() * self.per / price

		if buy in ('sell', 1):
			print('self.trader.sell_limit(\'%s\', %.8f, %.8f)' % (name, count, price))
		else:
			print('self.trader.buy_limit(\'%s\', %.8f, %.8f)' % (name, count, price))

		try:
			if buy in ('sell', 1):
				return self.trader.sell_limit(name, count, price)['result']['uuid']
			else:
				return self.trader.buy_limit(name, count, price)['result']['uuid']
		except:
			return 0

	def last(self, cur):
		cur = self.name(cur)

		y = []
		for i in self.trader.get_market_history(cur)['result']:
			y.append(i['Price'])

		pylab.plot([i for i in range(1, len(y) + 1)], y)
		pylab.grid(True)
		pylab.show()
		#pylab.savefig(cur + '.png', format='png', dpi=150)

	def all(self):
		s = 0
		for i in self.trader.get_balances()['result']:
			sell = self.price(i['Currency'], 1) * i['Balance']
			print(i['Currency'].lower(), i['Balance'], sell)
			s += sell
		print('--------------------')
		print('%fɃ\n%f₽' % (s, s / ru()))

	def order(self, id):
		try:
			if self.trader.get_order(id)['result']['Closed'] != None:
				return True
		except:
			pass
		return False

	def cancel(self, id):
		self.trader.cancel(id)

stock = [YoBit(), Bittrex()]