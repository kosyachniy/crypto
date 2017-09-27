#Работает с биржей, считывает операции
from yobit import *
from func import *

sendid = meid
trader = YoBit()

def trade():
	while True:
		with db:
			for i in db.execute("SELECT * FROM operations"): # WHERE time2='None'
				if i[11] == None: #оптимизировать
					name = currencies[i[2]][1].lower() + '_btc'
					res = trader.ticker(name)
					if res['success'] == 0:
						db.execute("UPDATE operations SET time2=0 WHERE id=(?)", (i[0],))
						bot.send_message(sendid, 'YoBit: Валюта не найдена (' + i[2] + ')')
					else:
						#Покупка / продажа + контроль ошибок
						bot.send_message(sendid, 'YoBit: Курс покупки: ' + res[name]['buy'] + ' | Курс продажи: ' + res[name]['sell'])