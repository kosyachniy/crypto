import sys
sys.path.append('../')

from datetime import datetime
time=datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

from crypto.func import *

with db:
	db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (0, 0, 0.0023, 0.0023)")
	db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (0, 1, 0.0023, 0.0023)")
	db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (0, 2, 0.0023, 0.0023)")
	db.execute("INSERT INTO lastmessage (id, chat, message) VALUES (-1001134090450, 608)")