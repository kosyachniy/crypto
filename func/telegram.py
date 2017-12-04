#Telegram
from func.data import db, exchangers
import json, telebot

exch = [i[0] for i in exchangers]

with open('data/keys.txt', 'r') as file:
	token = json.loads(file.read())['telegram']['bot']

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())['write']
	channelid = s['channel']
	twochannel = s['channelen']
	admin = s['admin']

bot = telebot.TeleBot(token)

#Меню
from telebot import types

def keyboard(*cat):
	x = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for j in cat:
		x.add(*[types.KeyboardButton('/' + i) for i in j])
	return x

def send(message, forward=0, group=0):
	if group:
		if not forward:
			bot.send_message(group, message)
		else:
			bot.forward_message(group, forward, message)
	else:
		if not forward:
			for i in admin:
				bot.send_message(i, message, reply_markup=keyboard(exch, ['PUMP', 'Информация']))
		else:
			for i in admin:
				try:
					bot.forward_message(i, forward, message)
				except:
					try:
						bot.send_message(i, db['messages'].find_one({'chat': forward, 'message': message})['text'])
					except:
						bot.send_message(i, str({'chat': group, 'message': message}))