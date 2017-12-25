#Операции с биржами
from func.data import *

'''
from celery.decorators import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery import Task
'''

history = db['history']

ru = lambda: float(requests.get('https://blockchain.info/tobtc?currency=RUB&value=1000').text) / 1000
us = lambda: float(requests.get('https://blockchain.info/tobtc?currency=USD&value=1').text)

from matplotlib import use
use('Agg')
import matplotlib.pyplot as plt
def graph(y, price, minutes=20):
	tim = {}
	for i in y[::-1]:
		if y[0][0] - i[0] <= minutes:
			if i[0] not in tim:
				tim[i[0]] = []
			tim[i[0]].append(i[1])

	startx = y[0][0]
	starty = tim[startx][-1]
	tim[startx+5] = [starty, starty, price, price]
	delt = min(set(tim)) - 1

	plt.clf()
	fig, ax = plt.subplots()

	bp = ax.boxplot([tim[i] if tim[i][0] > tim[i][-1] else [] for i in tim], positions=[int(i-delt) for i in tim], patch_artist=True)
	plt.setp(bp['boxes'], color='red')
	vp = ax.boxplot([tim[i] if tim[i][0] <= tim[i][-1] else [] for i in tim], positions=[int(i-delt) for i in tim], patch_artist=True)
	plt.setp(vp['boxes'], color='green')
	for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
		plt.setp(bp[element], color='black')
		plt.setp(vp[element], color='black')

	plt.annotate(u'Up', xy=(startx-delt, starty), xytext=(startx+5-delt, price), arrowprops={'arrowstyle': '<|-'})

	plt.grid(True)
	#plt.show()
	plt.savefig('re.png', format='png', dpi=150)

	return len(tim)

class YoBit():
	def __init__(self):
		from func.library.yobit import YoBit as t
		self.trader = t() #оптимизировать
		self.num = 0
		self.comm = 0.002
		self.min = 0.00011 #0.0001
		self.per = 0.03
		self.limit = 0.0001

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

	def us(self):
		return 1 / self.trader.ticker('btc_usd')['btc_usd']['buy']

	#Баланс валюты
	def info(self, cur='btc', attempt=0):
		#иногда возникает баг
		#учитывать, что может тратить те деньги, что сейчас на ордере -> ошибка
		try:
			if cur:
				return self.trader.get_info()['return']['funds_incl_orders'][cur]
			else:
				s = 0
				y = self.trader.get_info()['return']['funds']
				for i in y:
					price = self.price(i, 1)
					sell = price * y[i]
					if sell > self.min or i == 'rur':
						s += sell
				return s
		except:
			sleep(5)
			if attempt:
				return 0
			else:
				return self.info(cur, 1)

	#Курс
	def price(self, cur, buy='buy'):
		cur = self.name(cur)
		if not cur:
			return 1

		res = self.trader.ticker(cur)
		buy = self.buys(buy, 1 if cur != 'btc_rur' else 0)

		#Есть ли эта валюта на бирже
		if cur in res: #and res[cur][buy] >= self.limit: #проходит ли минимальный курс покупки # and (res[cur]['vol'] >= 1) #и достаточно ли объёма
			if cur == 'btc_rur':
				return 1 / res[cur][buy]
			return res[cur][buy]

		return 0

	#Купить / продать
	def trade(self, cur, count=0, price=0, buy='buy'):
		if not price: price = self.price(cur, buy)
		name = self.name(cur)
		if not count: count = self.info() * self.per / price
		price = '%.8f' % (price,)

		buy = self.buys(buy, 0 if cur != 'btc_rur' else 1)
		print('self.trader.trade(\'%s\', \'%s\', \'%s\', %.8f)' % (name, buy, price, count))

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
		formated = exchangers[self.num][0] + '\n--------------------\n'
		s = 0
		x = {}
		rub = self.ru()
		try:
			y = self.trader.get_info()['return']['funds']
		except:
			return None

		for i in y:
			price = self.price(i, 1)
			sell = price * y[i]
			if sell > self.min or i == 'rur':
				x[i] = [0, price, sell]
				s += sell

		for i in x:
			try:
				o = list(self.trader.active_orders(i+'_btc')['return'])[0]
			except:
				continue
			#print(o)
			try:
				id = history.find_one({'order': o})['message']
				price = history.find_one({'message': id, 'type': 'buy'})['price']
				x[i][0] = x[i][1] - price
			except:
				pass

		x = sorted([[x[i][2], i.upper(), x[i][0]] for i in x])[::-1]

		for i in x:
			ch = '↑' if i[2] > 0 else '↓' if i[2] < 0 else ''
			formated += '%s %s 	%fɃ 	(%d₽)\n' % (ch, i[1], i[0], i[0] / rub)

		formated += '--------------------\nИтог: %fɃ (%d₽)' % (s, s / rub)
		return formated

	def last(self, cur, price):
		cur = self.name(cur)
		y = self.trader.trades(cur, 500)[cur]
		y = [[i['timestamp'] // 60, i['price']] for i in y]
		return graph(y, price)

	def check(self, cur):
		cur = currencies[cur][1].lower()
		x = self.trader.get_info()['return']['funds_incl_orders']
		if cur in x and x[cur]:
			return x[cur]
		return 0

class Bittrex():
	def __init__(self):
		from func.library.bittrex import Bittrex as t
		self.num = 1
		self.trader = t() #оптимизировать
		self.comm = 0.002
		self.min = 0.00051 #0.0005
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

	def info(self, name='btc', attempt=0):
		try:
			if name:
				for i in self.trader.get_balances()['result']:
					if i['Currency'].lower() == name.lower():
						return i['Available']
			else:
				s = 0
				y = [i for i in self.trader.get_balances()['result'] if i['Balance']]
				z = {i['MarketName']: i['Bid'] for i in self.trader.get_market_summaries()['result']}

				for i in y:
					try:
						sell = i['Balance'] if i['Currency'] == 'BTC' else z['BTC-'+i['Currency']] * i['Balance'] if i['Currency'] != 'USDT' else i['Balance'] / z['USDT-BTC']
					except:
						continue
					if not sell:
						continue
					if sell > self.min:
						s += sell
				return s
		except:
			if attempt:
				return 0
			else:
				return self.info(name, 1)

	def ru(self):
		return ru()

	def us(self):
		return 1 / self.trader.get_ticker('usdt-btc')['result']['Bid']

	def price(self, cur, buy='buy'):
		if type(cur) == str:
			cur = cur.lower()
		if cur in ('btc', 0):
			return 1

		cur = self.name(cur)
		x = self.trader.get_ticker(cur)
		buy = self.buys(buy, 1)
		try:
			if x['success']:
				return x['result'][buy]
		except:
			pass

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
				x = self.trader.sell_limit(name, count, price)
				print(x)
				return x['result']['uuid']
			else:
				x = self.trader.buy_limit(name, count, price)
				print(x)
				return x['result']['uuid']
		except:
			return 0

	def order(self, id):
		try:
			if self.trader.get_order(id)['result']['Closed'] != None:
				return True
		except:
			pass
		return False

	def cancel(self, id):
		self.trader.cancel(id)

	def all(self):
		formated = exchangers[self.num][0] + '\n--------------------\n'
		s = 0
		x = {}
		rub = self.ru()

		y = [i for i in self.trader.get_balances()['result'] if i['Balance']]
		z = {i['MarketName']: i['Bid'] for i in self.trader.get_market_summaries()['result']}

		for i in y:
			price = 1 if i['Currency'] == 'BTC' else z['BTC-'+i['Currency']] if i['Currency'] != 'USDT' else 1 / z['USDT-BTC']
			sell = price * i['Balance']
			if not sell:
				continue
			if sell > self.min:
				x[i['Currency']] = [0, price, sell]
				s += sell

		for i in self.trader.get_open_orders()['result']:
			#print(i['OrderUuid'])
			try:
				id = history.find_one({'order': i['OrderUuid']})['message']
				price = history.find_one({'message': id, 'type': 'buy'})['price']
				x[i['Exchange'][4:]][0] = x[i['Exchange'][4:]][1] - price
			except:
				pass

		x = sorted([[x[i][2], i, x[i][0]] for i in x])[::-1]

		for i in x:
			ch = '↑' if i[2] > 0 else '↓' if i[2] < 0 else ''
			formated += '%s %s 	%fɃ 	(%d₽)\n' % (ch, i[1], i[0], i[0] / rub)

		formated += '--------------------\nИтог: %fɃ (%d₽)' % (s, s / rub)
		return formated

	def last(self, cur, price):
		cur = self.name(cur)
		y = self.trader.get_market_history(cur)['result']
		y = [[mktime(strptime(i['TimeStamp'].split('.')[0], '%Y-%m-%dT%H:%M:%S')) // 60, i['Price']] for i in y]
		return graph(y, price)

	def check(self, cur):
		cur = currencies[cur][1]
		x = self.trader.get_balances()['result']
		for i in x:
			if i['Currency'] == cur and i['Balance']:
				return i['Balance']
		return 0

stock = [YoBit(), Bittrex()]