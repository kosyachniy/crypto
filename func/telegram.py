#Telegram
from func.data import db, exchangers
import json, telebot

exch = [i[0] for i in exchangers]

with open('data/keys.txt', 'r') as file:
	token = json.loads(file.read())['telegram']['bot']

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())['write']
	channelid = s['channel']
	admin = s['admin']

bot = telebot.TeleBot(token)

#Меню
from telebot import types

def keyboard(chat, *cat):
	x = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for j in cat:
		x.add(*[types.KeyboardButton('/' + i) for i in j])
	return bot.send_message(chat, reply_markup=x)

def send(message, forward=0, group=0):
	if group:
		if not forward:
			bot.send_message(group, message)
		else:
			bot.forward_message(group, forward, message)
	else:
		if not forward:
			for i in admin:
				bot.send_message(i, message) #, reply_markup=keyboard()
				keyboard(i, exch, ['PUMP', 'Информация'])
		else:
			for i in admin:
				try:
					bot.forward_message(i, forward, message)
				except:
					try:
						bot.send_message(i, db['messages'].find_one({'chat': group, 'message': message})['text'])
					except:
						bot.send_message(i, 'Сообщение шифровано!')
				#keyboard(i, exch, ['PUMP', 'Информация'])