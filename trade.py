#Торговля по сигналам
from func import *

class YoBit():
	def __init__(self):
		from library.yobit import YoBit as t
		self.trader = t() #оптимизировать
		self.comm = 0.002

	def info(self):
		total = 0.02 #биткоинов на этой бирже
		return total

	def price(self, cur, buy):
		if cur == 0:
			return 1 #пока всё покупаем через биткоины

		name = currencies[cur][1].lower() + '_btc'
		res = self.trader.ticker(name)

		if name in res:
			return res[name]['sell'] if buy != 1 else res[name]['buy']

		#сразу выставлять на продажу по ключевым ценам + снимать если падает оредры и продавать по низкой

		return None

	def trade(self, cur, count, price, buy):
		name = currencies[cur][1].lower() + '_btc'
		buys = 'buy' if buy != 1 else 'sell'
		bot.send_message(sendid, 'self.trader.trade(\'%s\', \'%s\', %.8f, %.8f)' % (name, buys, price, count)) #
		if buy != 1:
			bot.send_message(sendid, 'self.trader.trade(\'%s\', \'sell\', %.8f, %.8f)' % (name, price * 1.1, count * 0.5)) #
			bot.send_message(sendid, 'self.trader.trade(\'%s\', \'sell\', %.8f, %.8f)' % (name, price * 1.15, count * 0.3)) #
			bot.send_message(sendid, 'self.trader.trade(\'%s\', \'sell\', %.8f, %.8f)' % (name, price * 1.2, count * 0.1)) #
			bot.send_message(sendid, 'self.trader.trade(\'%s\', \'sell\', %.8f, %.8f)' % (name, price * 1.25, count * 0.1)) #
		'''
		try:
			self.trader.trade(name, buys, price, count)
			if buy != 1:
				self.trader.trade(name, 'sell', price * 1.1, count * 0.5)
				self.trader.trade(name, 'sell', price * 1.15, count * 0.3)
				self.trader.trade(name, 'sell', price * 1.2, count * 0.1)
				self.trader.trade(name, 'sell', price * 1.25, count * 0.1)
		except:
			return 0
		else:
			return 1
		'''
		return 1
		#синхронизация по исполнению ордеров