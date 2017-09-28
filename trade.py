#Торговля по сигналам
from func import *
from library.yobit import *

trader = YoBit()

def info0():
	total = 0.02 #биткоинов на этой бирже
	return total

def price0(cur, buy):
	name = currencies[cur][1].lower() + '_btc'
	res = trader.ticker(name)

	if name in res:
		return res[name]['buy'] if buy != 1 else res[name]['sell']

	return None

def trade0(cur, count, price):
	#
	return 1 #успешно ли прошла операция на бирже + синхронизация в конце дня / по исполнению ордеров