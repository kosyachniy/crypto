from func.main import *
#from pump import pump

messages = db['messages']
exchangers = [i[0] for i in exchangers]

try:
	num = messages.find().sort('id', -1)[0]['id']
except:
	num = 0

#Меню
from telebot import types

def keyboard(chat, *cat):
	x = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for j in cat:
		x.add(*[types.KeyboardButton('/' + i) for i in j])
	return bot.send_message(chat, 'Меню:', reply_markup=x)

'''
@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.send_message(message.chat.id, 'Привет! Я авто-трейд бот на биржах криптовалют!\n\nНапиши мне сигнал и я выставлю ордеры на биржах, буду контроллировать их на стоп-лосс и исполнение.')
	if message.chat.id in admin:
		bot.send_message(message.chat.id, 'Присоединённые биржи: ...')
	else:
		bot.send_message(message.chat.id, 'Для пользования ботом, его нужно активировать. Свяжитесь с нами здесь: @kosyachniy')
'''

@bot.message_handler(commands=['main', 'Назад'])
def main(message):
	if message.chat.id in admin:
		keyboard(message.chat.id, exchangers, ['PUMP', 'Информация'])

@bot.message_handler(commands=['PUMP', 'pump', 'памп', 'ПАМП', 'Памп'])
def pumps(message):
	if message.chat.id in admin:
		#bot.send_message(message.chat.id, 'Памп на бирже: ')
		x = keyboard(message.chat.id, exchangers, ['Назад'])
		bot.register_next_step_handler(x, pumpss)

def pumpss(message):
	if message.chat.id in admin:
		bot.send_message(message.chat.id, '@zodzubot') #pump(message.text)

@bot.message_handler(commands=['Информация', 'Инфо', 'info'])
def info(message):
	if message.chat.id in admin:
		for i in stock:
			bot.send_message(message.chat.id, i.all())
		#main(message)

@bot.message_handler(commands=exchangers)
def stockss(message):
	if message.chat.id in admin:
		keyboard(message.chat.id, ['Сигнал', 'Покупка', 'Продажа', 'ПАМП', 'Инфо', 'Назад'])

#Дальнейшая обработка
@bot.message_handler(content_types=["text"])
def text(message):
	try:
		chat, id, text = message.forward_from_chat.id, message.forward_from_message_id, message.text
	except:
		chat, id, text = message.chat.id, message.message_id, message.text

	if message.chat.id in admin:
		#оптимизировать
		try:
			num = messages.find().sort('id', -1)[0]['id']
		except:
			num = 0
	
		num += 1
		doc = {'id': num, 'chat': chat, 'message': id, 'text': text}
		messages.insert(doc)
	else:
		bot.send_message(message.chat.id, 'У вас нет доступа!')

bot.polling(none_stop=True)