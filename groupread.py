from func.user import *

from_id = -1001149594247 #-1001143136828
to_id = 136563129 #440219158

for i in client.get_message_history(client.get_entity(from_id))[1]:
	#print(i)

	y = '%d %d\n' % (from_id, i.id)

	try:
		x = i.message
	except:
		x = ''

	try:
		x += i.media.caption
	except:
		pass

	#+изображения

	client.send_message(to_id, y + x + '\n--------------------')