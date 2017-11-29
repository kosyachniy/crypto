from func.data import db
from func.user import *
from time import sleep
import re

from_id = -1001149594247 #-1001143136828

messages = db['messages']

get = lambda x=1: client.get_message_history(client.get_entity(from_id), x)[1]

clean = lambda cont, words='': re.sub('[^a-zа-я' + words + ']', ' ', cont.lower()).split()
on = lambda x, y, words='': len(set(clean(x, words) if type(x) == str else x) & set(clean(y, words) if type(y) == str else y))

def autoadd():
	num = get()[0].id
	print('!', num) #

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

				print(text) #

				if on(text, ['#cryptosignals', '#иностранный', '#альтернативный', '#буржуйский', '#cryptosignalsio', '#cryptowolf', '#privatesignals', '#insighttradebot', '#premiumsignals'], '#'):
					try:
						id = messages.find().sort('id', -1)[0]['id']
					except:
						id = 0

					print(id+1)

					doc = {'id': id+1, 'chat': from_id, 'message': num, 'text': text}
					messages.insert(doc)

				num = i.id

		sleep(5)

if __name__ == '__main__':
	autoadd()