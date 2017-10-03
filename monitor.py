#Контроль сигналов
from func import *

#Данные
with open('data/vocabulary.txt', 'r') as file:
	vocabulary = json.loads(file.read())

on = lambda text, words: any([word in text for word in words])

alphabet = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъёфывапролджэячсмитьбю#'
clean = lambda cont, words: str(''.join([i if i in alphabet + words else ' ' for i in cont])).split()

def an(text, words):
	cur = 0
	text = clean(text, words)
	for j in range(1, len(currencies)):
		#print(text)
		if words + currencies[j][1].lower() in text or words + currencies[j][0].lower() in text:
			print(j, currencies[j])
			if not cur:
				cur = j + 0
			else:
				return -1
	return cur

def monitor():
		try:
			with open('data/trade.txt', 'r') as file:
				num = json.loads(file.read()[-1])['id']
		except:
			num = 0

		#Убирать ссылки (чтобы не путать лишними словами), VIP
		text = message.text.lower()
		print(text)
		#time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

		loss = [0, 0.9] #
		out = []
		vol = 0
		price = 0

#Распознание сигнала
		#Определение сигнал покупки / продажи
		if on(text, vocabulary['buy']):
			buy = 2
		elif on(text, vocabulary['sell']):
			buy = 1
		else:
			buy = 0

		#Распознание размеров

		#Определение биржи
		exc = -1
		for j in range(len(exchanges)):
			if exchanges[j][0].lower() in text:
				exc = j
				break

		#Определение срока
		if on(text, vocabulary['short']):
			term = 0
		elif on(text, vocabulary['medium']):
			term = 1
		elif on(text, vocabulary['long']):
			term = 2
		else:
			term = -1

		#Определение валюты
		cur = an(text, '#') #поиск по хештегу
		if cur <= 0: cur = an(text, '')
		if cur == -1: return 0 #если несколько валют

		print(cur, exc, term, buy)

		#Рассмотреть случай продажи валюты
		if cur >= 1 and buy != 1:
#Замены
			if not vol:
				vol = 0.03

			if not len(out):
				out = [
					[0.5, 0, 1.1],
					[0.3, 0, 1.15],
					[0.1, 0, 1.2],
					[0.1, 0, 1.25]
				]

#Отправка на обработку
			num += 1

			sett = {
				'id': num,
				'currency': cur,
				'exchanger': exc,
				'price': price,
				'volume': vol,
				'out': out,
				'loss': loss,
				'term': term,
				'chat': message.chat.id,
				'mess': message.message_id
			} #, 'time': time

			#Если без покупки, первые поля пустые ?
			with open('data/trade.txt', 'a') as file:
				print(json.dumps(sett), file=file)

if __name__ == '__main__':
	monitor()