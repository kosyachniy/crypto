#Контроль сигналов
from func import *
from yobit import *

#Данные
sendid = meid
trader = YoBit()

with open('data/vocabulary.txt', 'r') as file:
	vocabulary = json.loads(file.read())

on = lambda text, words: any([word in text for word in words])

alphabet = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъёфывапролджэячсмитьбю'
clean = lambda cont: str(''.join([i if i in alphabet else ' ' for i in cont])).split()

def monitor():
	while True:
#Список сообщений
		x = []
		with db:
			for i in db.execute("SELECT * FROM lastmessage"):
				chat, id = i
				text = ''

				try:
					text = bot.forward_message(meid, chat, id + 1).text
				except:
					try:
						text = bot.forward_message(meid, chat, id + 2).text
					except:
						id = 0
					else:
						id += 2
				else:
					id += 1

				if id:
					if text: #изображения
						x.append([chat, id, text.lower()])
					db.execute("UPDATE lastmessage SET message=(?) WHERE id=(?)", (id, chat))
				
				sleep(1)

		print(x)
		for i in x:
			buy = 0
			exc = 0
			cur = -1
			count = 1.0
			time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

#Распознание сигнала
			if on(i[2], vocabulary['buy']):
				buy = 2
			elif on(i[2], vocabulary['sell']):
				buy = 1
			else:
				buy = 0

			for j in range(len(exchanges)):
				if exchanges[j][0].lower() in i[2]:
					exc = j
					break

			t = 0
			for j in range(1, len(currencies)):
				text = clean(i[2])
				#print(text)
				if currencies[j][1].lower() in text or currencies[j][0].lower() in text:
					print(j, currencies[j])
					if t == 0:
						t = 1
					elif t == 1:
						t = 2
						break

					cur = j
			if t == 2: continue #

#
			if cur >= 1:
				name = currencies[cur][1].lower() + '_btc'
				res = trader.ticker(name)
				if name in res:
					#Покупка / продажа + контроль ошибок
					#db.execute("UPDATE operations SET count=(?), price=(?), time2=(?) WHERE id=(?)", (0, res[name]['buy'], time, i[0]))
					bot.send_message(sendid, 'YoBit - %s: %.10f - %.10f' % (currencies[cur][1], res[name]['buy'], res[name]['sell']))
				else:
					#db.execute("UPDATE operations SET time2=0 WHERE id=(?)", (i[0],))
					bot.send_message(sendid, 'YoBit - %s: Валюта не найдена' % currencies[cur][1]) #сделать неопределённую валюту с выводом в бота
				#db.execute("INSERT INTO operations (act, currency, changer, buy, per, meschat, mesid, time1) VALUES (1, ?, ?, ?, 0.03, ?, ?, ?)", (cur, exc, buy, chat, id, time))
			elif buy >= 1:
				bot.send_message(sendid, 'Не распознано')
				bot.forward_message(sendid, chat, id)

			sleep(5)

if __name__ == '__main__':
	monitor()