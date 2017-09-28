#Торговля по сигналам
from func import *

class YoBit():
	def __init__(self):
		from library.yobit import YoBit as t
		self.trader = t() #оптимизировать

	def info(self):
		total = 0.02 #биткоинов на этой бирже
		return total

	def price(self, cur, buy):
		if cur == 0:
			return 1 #пока всё покупаем через биткоины

		com = 1 - 0.002 #комиссия

		name = currencies[cur][1].lower() + '_btc'
		res = self.trader.ticker(name)

		if name in res:
			return res[name]['sell'] * com if buy != 1 else res[name]['buy'] * com

		#сразу выставлять на продажу по ключевым ценам + снимать если падает оредры и продавать по низкой

		return None

	def trade(self, cur, count, price):
		name = currencies[cur][1].lower() + '_btc'
		buys = 'buy' if buy != 1 else 'sell'
		#self.trader.trade(name, buys, price, count)
		return 1 #успешно ли прошла операция на бирже + синхронизация в конце дня / по исполнению ордеров