from func.data import db
from func.user import *

from_id = -1001149594247 #-1001143136828

messages = db['messages']

get = lambda x=1: client.get_message_history(client.get_entity(from_id), x)[1]

def autoadd():
	try:
		num = messages.find().sort('id', -1)[0]['message']
	except:
		num = 0

	while True:
		last = get()[0].id
		for i in get(last - num):
			if i.id > num:
				#print(i)

				try:
					text = i.message
				except:
					text = ' '

				try:
					text += i.media.caption
				except:
					pass

				#+изображения

				try:
					id = messages.find().sort('id', -1)[0]['id']
				except:
					id = 0

				doc = {'id': id, 'chat': from_id, 'message': num, 'text': text}
				messages.insert(doc)

				num = i.id

		sleep(5)

if __name__ == '__main__':
	autoadd()