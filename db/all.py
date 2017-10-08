import sys
sys.path.append('../')
#python3 ./-/create.py

from crypto.func import *

with db:
	db.execute("CREATE TABLE lastmessage (id INTEGER PRIMARY KEY, message int)")

	#db.execute("INSERT INTO lastmessage (id, message) VALUES (-1001141110698, 818)")
	db.execute("INSERT INTO lastmessage (id, message) VALUES (-1001134090450, 878)")
	db.execute("INSERT INTO lastmessage (id, message) VALUES (-1001122893891, 920)")
	db.execute("INSERT INTO lastmessage (id, message) VALUES (-1001133674353, 464)")