import json, requests, re
from time import sleep, gmtime
from datetime import datetime

#Данные
currencies = []
with open('data/currencies.txt', 'r') as file:
	for i in file:
		currencies.append(json.loads(i[:-1]))

with open('data/exchangers.txt', 'r') as file:
	exchangers = json.loads(file.read())

with open('data/set.txt', 'r') as file:
	utc = json.loads(file.read())['utc']

#MongoDB
from pymongo import MongoClient
db = MongoClient()['crypto']