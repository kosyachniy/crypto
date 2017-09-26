import sys
sys.path.append('../')
from crypto.func import *

with db:
	db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (0, 0, 0.02, 0.02)")
	db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (0, 1, 0.02, 0.02)")
	db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (0, 2, 0.02, 0.02)")
	db.execute("INSERT INTO lastmessage (id, message) VALUES (-1001134090450, 500)")