#Торговля по сигналам
from func import *

class YoBit():
	def __init__(self):
		from library.yobit import YoBit as t
		self.trader = t() #оптимизировать
		self.comm = 0.002

	#Преобразовать индекс / название валюты для биржи
	def name(cur):
		if type(cur) == str:
			return cur.lower() + '_btc'
		else:
			return currencies[cur][1].lower() + '_btc'

	#Весь баланс
	all = lambda self: list(self.trader.get_info()['return']['funds'].items())

	#Количество данной валюты у меня
	info = lambda self, cur='btc': self.trader.get_info()['return']['funds'][cur]

	def price(self, cur, buy):
		if cur == 0:
			return 1 #пока всё покупаем через биткоины
		cur = name(cur)
		res = self.trader.ticker(cur)

		if cur in res:
			return res[cur]['sell'] if buy != 1 else res[cur]['buy']

		#сразу выставлять на продажу по ключевым ценам + снимать если падает оредры и продавать по низкой

		return None

	#Купить / продать
	def trade(self, cur, count, price, buy):
		name = name(cur)
		buys = 'buy' if buy != 1 else 'sell'
		bot.send_message(sendid, 'self.trader.trade(\'%s\', \'%s\', %.8f, %.8f)' % (name, buys, price, count)) #
		if buy != 1:
			bot.send_message(sendid, 'self.trader.trade(\'%s\', \'sell\', %.8f, %.8f)' % (name, price * 1.1, count * 0.5)) #
			bot.send_message(sendid, 'self.trader.trade(\'%s\', \'sell\', %.8f, %.8f)' % (name, price * 1.15, count * 0.3)) #
			bot.send_message(sendid, 'self.trader.trade(\'%s\', \'sell\', %.8f, %.8f)' % (name, price * 1.2, count * 0.1)) #
			bot.send_message(sendid, 'self.trader.trade(\'%s\', \'sell\', %.8f, %.8f)' % (name, price * 1.25, count * 0.1)) #
		'''
		try:
			q = self.trader.trade(name, buys, price, count)
			if 'success' not in q:
				return 0, 0, 0, 0, 0
			qm = [0, 0, 0, 0]
			if buy != 1:
				qm[0] = self.trader.trade(name, 'sell', price * 1.1, count * 0.5)
				qm[1] = self.trader.trade(name, 'sell', price * 1.15, count * 0.3)
				qm[2] = self.trader.trade(name, 'sell', price * 1.2, count * 0.1)
				qm[3] = self.trader.trade(name, 'sell', price * 1.25, count * 0.1)
		except:
			return 0, 0, 0, 0, 0
		else:
			qm = [i['return']['order_id'] if 'success' in i else 0 for i in qm]
			return q['return']['order_id'], *qm
		'''
		return 1, 1, 1, 1, 1
		#синхронизация по исполнению ордеров

	#Умная (быстрая) покупка / продажа
	def real(self, cur, buy='buy', price=0): #sell
		cur = name(cur)

		if price == 0:
			price = self.trader.ticker(cur)[cur]['sell' if buy == 'buy' else 'buy']
		#price = self.trader.ticker(cur)[cur]['last']

		if buy == 'buy':
			total = self.trader.get_info()['return']['funds']['btc']
			count = total * 0.05 / price
			delta = total * 0.03
		else:
			count = self.trader.get_info()['return']['funds'][cur[:-4]]
			delta = count * price 


		print('%.8f\n%.8f\n%.8f' % (price, count, delta))

		self.trader.trade(cur, buy, price, count)
		'''
		if buy == 'buy':
			sleep(30) #ждём пока исполнится ордер -> сделать в проверке ордера
			self.trader.trade(cur, 'sell', price * 1.1, count * 0.5)
			self.trader.trade(cur, 'sell', price * 1.15, count * 0.3)
			self.trader.trade(cur, 'sell', price * 1.2, count * 0.1)
			self.trader.trade(cur, 'sell', price * 1.25, count * 0.1)
		'''