from func import *

def autoadd():
	while True:
		with db:
			for i in db.execute("SELECT * FROM lastmessage"):
				chat, id = i
				text = ''

				try:
					text = bot.forward_message(meid, chat, id + 1).text
				except:
					try:
						text = bot.forward_message(meid, chat, id + 2).text
					except:
						id = 0
					else:
						id += 2
				else:
					id += 1

				if id:
					if text: #изображения
						with open('data/messages.txt', 'a') as file:
							print(json.dumps([chat, id, text.lower()], ensure_ascii=False), file=file)
					db.execute("UPDATE lastmessage SET message=(?) WHERE id=(?)", (id, chat))
				
				sleep(5)

if __name__ == '__main__':
	autoadd()