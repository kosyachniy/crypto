#Контроль сигналов
from func.data import *
from func.trade import stock
import math

#Данные
with open('data/vocabulary.txt', 'r') as file:
	vocabulary = json.loads(file.read())

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())
	reloss = [0, s['default']['stop-loss']]
	outd = s['default']['sell']
	outg = s['default']['gell']
	vold = s['default']['volume']
	veri = s['read']['reliable']
	unveri = s['read']['unreliable']

clean = lambda cont, words='': re.sub('[^a-zа-я' + words + ']', ' ', cont.lower()).split()
on = lambda x, y, words='': len(set(clean(x, words) if type(x) == str else x) & set(clean(y, words) if type(y) == str else y))
#on = lambda a, b: 1 if any([i in a for i in b]) else 0 #len(set(clean(a)) & set(b))

def an(text, words, stop):
	cur = 0
	text = clean(text, words)
	for j in range(1, len(currencies)):
		if words + currencies[j][1].lower() in text or (words + currencies[j][0].lower() in text and currencies[j][0].lower() not in stop):
			print(j, currencies[j])
			if not cur:
				cur = j + 0
			else:
				return -1
	return cur

def stoploss(text, catch):
	try:
		if '%' in text:
			l = 1 - int(re.findall(r'\d+', text)[0]) / 100
			if l < 0: return catch
			return [0, l]
		elif '.' in text:
			return [1, float(re.search(r'-?\d+\.\d*', text).group(0))]
	except:
		return catch

def seller(text):
	if '%' in text:
		return [0, 0, 1 + int(re.findall(r'\d+', text)[0]) / 100]
	else:
		return [0, 1, float(re.search(r'-?\d+\.\d*', text).group(0))]

def recognize(i):
	#Убирать ссылки (чтобы не путать лишними словами), VIP
	text = i['text'].lower().replace(',', '.') #Сделать замену запятой на точку
	print(text)
	#time = strftime('%d.%m.%Y %H:%M:%S')

	loss = reloss + []
	out = []
	vol = 0
	price = 0
	safe = 1 if on(text, veri, '#') else 0
	unsafe = 1 if on(text, unveri, '#') else 0

#Распознание сигнала
	#Условия необработки
	if on(text, vocabulary['stop'], '🚀$') or (len(clean(text)) * 1.5 > len(text) and len(text) > 70):
		return None

	#Определение сигнал покупки / продажи
	if on(text, vocabulary['buy']):
		buy = 2
	elif on(text, vocabulary['sell']):
		buy = 1
	else:
		buy = 0
	print('Type:', buy)

	#Определение биржи
	exc = -1
	for j in range(len(exchangers)):
		if exchangers[j][0].lower() in text:
			exc = j
			break
	print('Exchanger', exc)

	#Определение срока
	if on(text, vocabulary['short']):
		term = 0
	elif on(text, vocabulary['medium']):
		term = 1
	elif on(text, vocabulary['long']):
		term = 2
	else:
		term = -1
	print('Term:', term)

	#Определение валюты
	cur = an(text, '#', ['status']) #поиск по хештегу
	if cur <= 0: cur = an(text, '', ['status']) #сделать список стоп слов, которые не учитываются в поиске валют
	if cur in (-1, 0): return None #если несколько валют
	print('Currency:', cur)

	#Распознание размеров
	if ('\n' not in text) or (on(text, vocabulary['loss']) and text.count('\n') == 1):
		t = True
		text = text.split('\n')
		for j in clean(text[0], '.%0123456789'):
			try:
				if t:
					if '.' in j:
						price = float(j)
						t = False
				else:
					out.append(seller(j))
			except:
				pass
		if len(text) >= 2 and on(text[1], vocabulary['loss']):
			loss = stoploss(text[1], loss)
	else:
		for j in text.split('\n'):
			try:
				if on(j, vocabulary['buy']):
					price = float(re.search(r'-?\d+\.\d*', j).group(0))
					#Добавить разделение на несколько покупок
				elif on(j, vocabulary['sell']):
					out.append(seller(j))
			except:
				pass

		#Определение стоп-лосса
		for j in text.split('\n'):
			if on(j, vocabulary['loss']):
				loss = stoploss(j, loss)

	#Рассмотреть случай продажи валюты
	if buy != 1:
#Замены
		#Биржа
		if exc == -1:
			exc = excd #Биржа по умолчанию
		#i['exchanger'] = excd

		#Если вылюта уже имеется
		if stock[exc].check(cur): return None

		#Цена
		realprice = stock[exc].price(cur)

		#Если не указана цена покупки или сигнал недоверенный
		print('Price:', price)
		if not price or unsafe:
			price = realprice
		print('Price:', price)

		#Если не указаны объёмы покупки
		if not vol:
			vol = vold * 2 if safe else vold #vold * (safe + 1)
		print('Volume:', vol)

		#Если не указаны ордеры на продажу
		if not len(out):
			out = outg if safe else outd

		#Если указаны неправильные объёмы продажи #замены
		print('Sell:', out)
		zam = False
		for j in out:
			if (not j[1] and j[2] < 1) or (j[1] and realprice and j[2] < realprice):
				return None #zam = True
		if zam:
			out = outg if safe else outd

		#Если не указаны объёмы продажи
		if not out[0][0]:
			s = 0
			for j in range(len(out)):
				s += math.exp(j)
			x = 1 / s
			a = 0
			for j in range(len(out) - 1):
				out[-1 * (j + 1)][0] = round(math.exp(j) * x, 2)
				a += out[len(out) - j - 1][0]
			out[0][0] = 1 - a
		print('Sell:', out)

		#Последняя продажа = 100 - сумма остальных для определённых в сигнале объёмов

		#Если неправильно определил стоп-лосс
		print('Stop-loss:', loss)
		if loss[0] and realprice <= loss[1]:
			return None
		if (loss[0] and realprice and loss[1] >= realprice * reloss[1]) or (not loss[0] and loss[1] >= reloss[1]): #замены
			loss = reloss
		print('Stop-loss:', loss)

#Отправка на обработку
		sett = {
			'id': i['id'],
			'currency': cur,
			'exchanger': exc,
			'price': price,
			'realprice': realprice,
			'volume': vol,
			'out': out,
			'loss': loss,
			'term': term,
			'chat': i['chat'],
			'mess': i['message'],
			'safe': safe
		} #, 'time': time

		#Если без покупки, первые поля пустые ?
		return sett

def monitor():
#БД
	messages = db['messages']
	trade = db['trade']
	settings = db['set']

#Первоначальные значения
	try:
		num = messages.find().sort('id', -1)[0]['id']
	except:
		num = 0

#Список новых сигналов
	while True:
		x = [i for i in messages.find({'id': {'$gt': num}})]

		try:
			jump = settings.find_one({'name': 'jump'})['cont']
		except:
			jump = 0

#Обработка
		for i in x:
			num = i['id']

			if jump != 1: #если продажа
				x = recognize(i)
				if x: trade.insert(x)

if __name__ == '__main__':
	monitor()