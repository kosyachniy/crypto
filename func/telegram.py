#Telegram
import json, telebot

from func.data import exchangers

with open('data/keys.txt', 'r') as file:
	token = json.loads(file.read())['telegram']['bot']

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())['write']
	channelid = s['channel']
	admin = s['admin']

bot = telebot.TeleBot(token)

'''
#Меню
from telebot import types

def keyboard():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*[types.KeyboardButton(i) for i in exchangers])
	keyboard.add(*[types.KeyboardButton(i) for i in ['PUMP', 'Информация']])
'''

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
		else:
			for i in admin:
				try:
					bot.forward_message(i, forward, message)
				except:
					bot.send_message(i, 'Сообщение шифровано!')