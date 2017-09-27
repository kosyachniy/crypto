#Работает с биржей, считывает операции
from yobit import *
from func import *

sendid = meid
trader = YoBit()

def get():
	try:
		with db:
			return db.execute("SELECT * FROM operations")
	except:
		return get()

def update1(count, price, time2, id):
	try:
		with db:
			db.execute("UPDATE operations SET count=(?), price=(?), time2=(?) WHERE id=(?)", (count, price, time2, id))
	except:
		update1(count, price, time2, id)

def update2(id):
	try:
		with db:
			db.execute("UPDATE operations SET time2=0 WHERE id=(?)", (id,))
	except:
		update2(id)

def trade():
	while True:
		for i in get(): # WHERE time2='None'
			if i[11] == None: #оптимизировать
				name = currencies[i[2]][1].lower() + '_btc'
				res = trader.ticker(name)
				if name in res:
					time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
					#Покупка / продажа + контроль ошибок
					update1(0, res[name]['buy'], time, i[0])
					bot.send_message(sendid, 'YoBit - %s: %.10f - %.10f' % (currencies[i[2]][1], res[name]['buy'], res[name]['sell']))
				else:
					update2(i[0])
					bot.send_message(sendid, 'YoBit - %s: Валюта не найдена' % currencies[i[2]][1])