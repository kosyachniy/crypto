import sys
sys.path.append('../')
#python3 ./-/create.py

from crypto.func import *

with db:
	db.execute("CREATE TABLE currencies (id INTEGER PRIMARY KEY AUTOINCREMENT, currency int, changer int, count real, price real, loss real, half real, full real, term int, time time, succ int, sell1 int, sell2 int, sell3 int, sell4 int)")
	#db.execute("CREATE TABLE operations (id INTEGER PRIMARY KEY AUTOINCREMENT, act int, currency int, changer int, buy int, per real, count real, price real, meschat int, mesid int, time time)")
	db.execute("CREATE TABLE lastmessage (id INTEGER PRIMARY KEY, message int)")