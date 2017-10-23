import json, urllib, telebot, requests #, sqlite3
from time import sleep, gmtime
from datetime import datetime
#from bs4 import BeautifulSoup
from pymongo import MongoClient

#Данные
currencies = []
with open('data/currencies.txt', 'r') as file:
	for i in file:
		currencies.append(json.loads(i[:-1]))

with open('data/exchangers.txt', 'r') as file:
	exchanges = json.loads(file.read())

#Telegram
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

#SQLite
#db=sqlite3.connect('data/main.db', check_same_thread=False))

#MongoDB
db = MongoClient()['crypto']
table = db['history']

#Биржа
from functrade import *
stock = [YoBit(), Bittrex()]