from func.data import db
from func.user import *

messages = db['messages']
try:
	id = messages.find().sort('id', -1)[0]
except:
	id = 0

from_id = -1001149594247 #-1001143136828

get = lambda x=1: client.get_message_history(client.get_entity(from_id), x)[1]

def autoadd():
	channels = db['channels']
	num = 0
	for i in channels.find({'id': from_id}):
		num = i['message']
	if not num:
		channels.save({'id': from_id, 'message': get()[0].id})

	while True:
		last = get()[0].id
		for i in get(last - num):
			if i.id > num:
				#print(i)

				try:
					x = i.message
				except:
					x = ' '

				try:
					x += i.media.caption
				except:
					pass

				#+изображения

				doc = {'id': id, 'chat': from_id, 'message': id, 'text': text}
				messages.insert(doc)
				'''
				if text:
					with open('data/messages.txt', 'a') as file:
						print(json.dumps([chat, id, text.lower()], ensure_ascii=False), file=file)
				db.execute("UPDATE lastmessage SET message=(?) WHERE id=(?)", (id, chat))
				'''
		
		if last > num:
			channels.save({})

		sleep(5)

if __name__ == '__main__':
	autoadd()