from func.main import *

try:
	num = messages.find_one({'$orderby': {'_id': -1}})['id']
except:
	num = 0

#Меню
from telebot import types

def keyboard(chat):
	x = types.ReplyKeyboardMarkup(resize_keyboard=True)
	x.add(*[types.KeyboardButton('/' + i[0]) for i in exchangers])
	x.add(*[types.KeyboardButton('/' + i) for i in ['PUMP', 'Информация']])
	bot.send_message(chat, 'Меню:', reply_markup=x)

'''
@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.send_message(message.chat.id, 'Привет! Я авто-трейд бот на биржах криптовалют!\n\nНапиши мне сигнал и я выставлю ордеры на биржах, буду контроллировать их на стоп-лосс и исполнение.')
	if message.chat.id in admin:
		bot.send_message(message.chat.id, 'Присоединённые биржи: ...')
	else:
		bot.send_message(message.chat.id, 'Для пользования ботом, его нужно активировать. Свяжитесь с нами здесь: @kosyachniy')
'''

@bot.message_handler(commands=['main', 'info'])
def start(message):
	if message.chat.id in admin:
		bot.send_message(message.chat.id, 'Главный экран!')
		keyboard(message.chat.id)

@bot.message_handler(commands=['PUMP', 'pump'])
def start(message):
	if message.chat.id in admin:
		bot.send_message(message.chat.id, 'Главный экран!')
		keyboard(message.chat.id)

@bot.message_handler(content_types=["text"])
def text(message):
	try:
		chat, id, text = message.forward_from_chat.id, message.forward_from_message_id, message.text
	except:
		chat, id, text = message.chat.id, message.message_id, message.text

	if chat in admin:
		pass

bot.polling(none_stop=True)