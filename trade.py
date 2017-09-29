#Торговля по сигналам
from func import *

class YoBit():
	def __init__(self):
		from library.yobit import YoBit as t
		self.trader = t() #оптимизировать
		self.comm = 0.002

	def info(self):
		return self.trader.get_info()['return']['funds']['btc'] #биткоинов на этой бирже

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

	def real(self, cur, buy='buy'): #sell
		cur = cur.lower() + '_btc'
		total = self.trader.get_info()['return']['funds']['btc']
		price = self.trader.ticker(cur)[cur]['sell' if buy == 'buy' else 'buy']
		count = total * 0.05 / price

		print('%.8f\n%.8f\n%.8f' % (price, count, total * 0.03))

		print(self.trader.trade(cur, buy, price, count))
		sleep(30) #ждём пока исполнится ордер -> сделать в проверке ордера
		'''
		if buy == 'buy':
				self.trader.trade(cur, 'sell', price * 1.1, count * 0.5)
				self.trader.trade(cur, 'sell', price * 1.15, count * 0.3)
				self.trader.trade(cur, 'sell', price * 1.2, count * 0.1)
				self.trader.trade(cur, 'sell', price * 1.25, count * 0.1)
		'''