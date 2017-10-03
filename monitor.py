#Контроль сигналов
from func import *

#Данные
with open('data/vocabulary.txt', 'r') as file:
	vocabulary = json.loads(file.read())

on = lambda text, words: any([word in text for word in words])

alphabet = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъёфывапролджэячсмитьбю'
clean = lambda cont: str(''.join([i if i in alphabet else ' ' for i in cont])).split()

ru = lambda: float(requests.get('https://blockchain.info/tobtc?currency=RUB&value=1000').text) / 1000

def monitor():
	@bot.message_handler(content_types=["text"])
	def text(message):
		try:
			with open('data/trade.txt', 'r') as file:
				num = json.loads(file.read()[-1])['id']
		except:
			num = 0

		#Убирать ссылки (чтобы не путать лишними словами), VIP
		text = message.text.lower()
		print(text)
		exc = -1
		cur = -1
		#time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

		loss = [0, 0.9] #
		out = []
		vol = 0
		price = 0

#Распознание сигнала
		if on(text, vocabulary['buy']):
			buy = 2
		elif on(text, vocabulary['sell']):
			buy = 1
		else:
			buy = 0
		#Распознание размеров

		for j in range(len(exchanges)):
			if exchanges[j][0].lower() in text:
				exc = j
				break

		if on(text, vocabulary['short']):
			term = 0
		elif on(text, vocabulary['medium']):
			term = 1
		elif on(text, vocabulary['long']):
			term = 2
		else:
			term = -1

		#Добавить проверку есть ли одна валюта с хештегом, если нет перебирать все
		t = 0
		text = clean(text)
		for j in range(1, len(currencies)):
			#print(text)
			if currencies[j][1].lower() in text or currencies[j][0].lower() in text:
				print(j, currencies[j])
				if t == 0:
					t = 1
				elif t == 1:
					t = 2
					break

				cur = j
		if t == 2: return 0 #

		print(cur, exc, term, buy)

		#Рассмотреть случай продажи валюты
		if cur >= 0 and buy != 1:
#Замены
			if exc == -1: exc = 0 #Биржа по умолчанию
			exc = 0 #Временная замена на одну биржу

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
	bot.polling(none_stop=True)