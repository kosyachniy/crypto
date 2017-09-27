import sys
sys.path.append('../')
#python3 ./-/create.py

from crypto.func import *

with db:
	db.execute("CREATE TABLE currencies (id INTEGER PRIMARY KEY AUTOINCREMENT, currency int, changer int, count real, price real, loss real, half real, full real, time time)")
	db.execute("CREATE TABLE operations (id INTEGER PRIMARY KEY AUTOINCREMENT, act int, currency int, changer int, buy int, count real, price real, time time, total real, delta real)")
	db.execute("CREATE TABLE lastmessage (id INTEGER PRIMARY KEY, message int)")