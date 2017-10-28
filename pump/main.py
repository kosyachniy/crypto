import sys
sys.path.append('..')

from func.telegram import *
from pump.pump import pump
from pump.recognize import recognize

chat, id = -1001133674353, 884
meid = 136563129

def autoadd():
	while True:
		t = False
		for i in range(1, 6):
			try:
				text = bot.forward_message(meid, chat, id + i).document.file_id #.text
			except:
				continue
			else:
				id = id + i
				t = True
				break

		if t:
			print(t)
			'''
			file_info = bot.get_file(message.document.file_id)
			downloaded_file = bot.download_file(file_info.file_path)
			pump(recognize())
			'''

if __name__ == '__main__':
	autoadd()