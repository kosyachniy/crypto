#Telegram
import json, telebot

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())
	token = s['token']
	channelid = s['channelid']
	meid = s['meid']
	soid = s['soid']
bot = telebot.TeleBot(token)

def send(message, forward=0, group=0):
	if group:
		if not forward:
			bot.send_message(group, message)
		else:
			bot.forward_message(group, forward, message)
	else:
		if not forward:
			bot.send_message(meid, message)
			bot.send_message(soid, message)
		else:
			bot.forward_message(meid, forward, message)
			bot.forward_message(soid, forward, message)