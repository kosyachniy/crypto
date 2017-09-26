import sys
sys.path.append('../')
from crypto.func import *

with db:
	db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (-1, 0, 0.023, 0.0023)")
	db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (-1, 1, 0.023, 0.0023)")
	db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (-1, 2, 0.023, 0.0023)")
	db.execute("INSERT INTO lastmessage (id, message) VALUES (-1001134090450, 500)")