import sys
sys.path.append('../')

from crypto.func import *

with db:
	for i in db.execute("SELECT * FROM lastmessage"): print(i)