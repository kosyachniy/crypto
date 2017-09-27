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
					if name in res:
						time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
						#Покупка / продажа + контроль ошибок
						db.execute("UPDATE operations SET count=(?), price=(?), time2=(?) WHERE id=(?)", (0, res[name]['buy'], time, i[0]))
						bot.send_message(sendid, 'YoBit - %s: Курс покупки: %.10f | Курс продажи: %.10f' % (currencies[i[2]][1], res[name]['buy'], res[name]['sell']))
					else:
						db.execute("UPDATE operations SET time2=0 WHERE id=(?)", (i[0],))
						bot.send_message(sendid, 'YoBit - %s: Валюта не найдена' % currencies[i[2]][1])