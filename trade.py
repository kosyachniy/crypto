#Торговля по сигналам
from func import *

class YoBit():
	def __init__(self):
		from library.yobit import YoBit as t
		self.trader = t()

	def info(self):
		total = 0.02 #биткоинов на этой бирже
		return total

	def price(self, cur, buy):
		name = currencies[cur][1].lower() + '_btc'
		res = self.trader.ticker(name)

		if name in res:
			return res[name]['buy'] if buy != 1 else res[name]['sell']

		return None

	def trade(self, cur, count, price):
		#
		return 1 #успешно ли прошла операция на бирже + синхронизация в конце дня / по исполнению ордеров