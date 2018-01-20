#Контроль сигналов
from func.data import *
from func.trade import stock
import math

#Данные
currencies = [[i[0].lower(), i[1].lower()] for i in currencies]

with open('data/vocabulary.txt', 'r', encoding='utf-8') as file:
	vocabulary = json.loads(file.read())

with open('data/set.txt', 'r', encoding='utf-8') as file:
	s = json.loads(file.read())
	reloss = [0, s['default']['stop-loss']]
	outd = s['default']['sell']
	outg = s['default']['gell']
	vold = s['default']['volume']
	veri = s['read']['reliable']
	unveri = s['read']['unreliable']
	exception = s['read']['not_currency']

clean = lambda cont, words='': re.sub('[^a-zа-я' + words + ']', ' ', cont.lower()).split() if type(cont) == str else cont
on = lambda x, y, words='': len(set(clean(x, words)) & set(clean(y, words)))

#Распознание сигнала (строгое вычленение ключевой информации из текста)
def recognize(text):
	def an(text, words, stop):
		cur = 0
		text = clean(text, words+'0-9')
		for i, j in enumerate(currencies[1:]):
			if (words + j[0] in text and words + j[0] not in stop) or (words + j[1] in text and words + j[1] not in stop):
				print(i+1, j)
				if not cur:
					cur = i + 1
				else:
					return -1
		return cur

	def stoploss(text, catch):
		try:
			if '%' in text:
				l = 1 - int(re.findall(r'\d+', text)[0]) / 100
				return catch if l < 0 else [0, l]
			elif '.' in text:
				return [1, float(re.search(r'-?\d+\.\d*', text).group(0))]
		except:
			return catch

	def seller(text):
		if '%' in text:
			return [0, 0, 1 + int(re.findall(r'\d+', text)[0]) / 100]
		else:
			return [0, 1, float(re.search(r'-?\d+\.\d*', text).group(0))]

	#print(text)
	text = text.lower().replace(',', '.')
	#Убирать ссылки (чтобы не путать лишними словами), VIP
	#time = strftime('%d.%m.%Y %H:%M:%S')

	loss = -1
	out = []
	vol = 0
	price = 0

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
	print('Exchanger:', exc)

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
	cur = an(text, '#', exception) #поиск по хештегу
	if cur <= 0: cur = an(text, '', exception) #сделать список стоп слов, которые не учитываются в поиске валют
	if cur in (-1, 0): return None #если несколько валют
	print('Currency:', cur)

	#Распознание размеров
	texted = text.split('\n')
	if ('\n' not in text) or (on(text, vocabulary['loss']) and text.count('\n') == 1):
		t = True
		for j in clean(texted[0], '.%0123456789'):
			try:
				if t:
					if '.' in j:
						price = float(j)
						t = False
				else:
					out.append(seller(j))
			except:
				pass
		if len(texted) >= 2 and on(texted[1], vocabulary['loss']):
			loss = stoploss(texted[1], loss)
	else:
		for j in texted:
			try:
				if on(j, vocabulary['buy']):
					price = float(re.search(r'-?\d+\.\d*', j).group(0))
					#Добавить разделение на несколько покупок
				elif on(j, vocabulary['sell']):
					out.append(seller(j))
			except:
				pass

		#Определение стоп-лосса
		for j in texted:
			if on(j, vocabulary['loss']):
				loss = stoploss(j, loss)

	print('Price:', price)
	print('Sell:', out)

	#Рассмотреть случай продажи валюты
	if buy != 1:

#Отправка на обработку
		x = {
			'text': text,
			'currency': cur,
			'exchanger': exc,
			'price': price,
			'volume': vol,
			'out': out,
			'loss': loss,
			'term': term
		} #, 'time': time

		#Если без покупки, первые поля пустые ?
		return x

import time #

#Замены (замена неверной информации и переопределение под разными условиями и ограничениями)
def replacements(x):
	#Если не определена продажа
	if x['loss'] == -1:
		x['loss'] = reloss + []

	#Надёжность (проверенность / доверенность) сигналу #Переделать -> ИИ
	x['safe'] = 1 if on(x['text'], veri, '#') else -1 if on(x['text'], unveri, '#') else 0

	#Цена
	x['realprice'] = realprice = stock[x['exchanger'] if x['exchanger'] != -1 else x['exchanger']].price(x['currency'])

	#Биржа
	if x['exchanger'] == -1 and realprice:
		x['exchanger'] = excd #Биржа по умолчанию
	#exc = excd

	#Если вылюта уже покупалась
	if stock[x['exchanger']].check(x['currency']) * realprice > stock[x['exchanger']].min: return None

	#Если не указана цена покупки
	if not x['price']:
		x['price'] = realprice
	print('Price:', x['price'])

	#Если не указаны объёмы покупки
	if not x['volume']:
		x['volume'] = vold * 2 if x['safe'] == 1 else vold #vold * (safe + 1)
	print('Volume:', x['volume'])

	#Если не указаны ордеры на продажу или сигнал недоверенный
	if not len(x['out']) or x['safe'] == -1:
		x['out'] = outg if x['safe'] == 1 else outd
	else:
		#Если указаны неправильные объёмы продажи
		#zam = False
		for j in x['out']:
			if (not j[1] and x['price'] * j[2] < realprice) or (j[1] and realprice and j[2] < realprice): #j[2] < 1
				return None #zam = True
		#if zam: x['out'] = outg if x['safe'] == 1 else outd
		#Продумать слуяай, когда продажа и покупка указаны не верно
		#Продумать случай, когда уже произошёл этот рост

		#Если не указаны объёмы продажи
		if not x['out'][0][0]:
			y = 1 / sum((math.exp(j) for j in range(len(x['out']))))
			a = 0
			for j in range(len(x['out']) - 1):
				x['out'][-1 * (j + 1)][0] = round(math.exp(j) * y, 2)
				a += x['out'][len(x['out']) - j - 1][0]
			x['out'][0][0] = 1 - a
	print('Sell:', x['out'])

	#Последняя продажа = 100 - сумма остальных для определённых в сигнале объёмов

	#Если неправильно определил стоп-лосс
	print('Stop-loss:', x['loss'])
	if x['loss'] != None and x['loss'][0] and realprice <= x['loss'][1]:
		return None
	if x['loss'] == None or (x['loss'][0] and realprice and x['loss'][1] >= realprice * reloss[1]) or (not x['loss'][0] and x['loss'][1] >= reloss[1]): #замены
		x['loss'] = reloss
	print('Stop-loss:', x['loss'])

	return x

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
		'''
		try:
			jump = settings.find_one({'name': 'jump'})['cont']
		except:
			jump = 0
		'''

#Обработка
		for i in messages.find({'id': {'$gt': num}}):
			num = i['id']
			print('-' * 100, '\nMessage: ', num) #

			#Временное ограничение на какие-либо действия
			'''
			if jump == 1:
				print('Сигнал отвергнут из-за ограничений!')
				continue
			'''

			x = recognize(i['text'])
			if x:
				x = replacements(x)
				if x:
					x['chat'] = i['chat']
					x['mess'] = i['message']
					x['id'] = i['id']
					del x['text']
					trade.insert(x)
				else:
					print('Сигнал отвергнут после замен!')
			else:
				print('Сигнал отвергнут после распознания!')

if __name__ == '__main__':
	monitor()