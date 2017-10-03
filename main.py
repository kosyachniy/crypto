from multiprocessing import Process

from autoadd import autoadd
from monitor import monitor
from bot import bott

p1 = Process(target=autoadd)
p2 = Process(target=monitor)
p3 = Process(target=bott)

p1.start()
p2.start()
p3.start()

#Нельзя повторять одни и те же сигналы!
#Управление ботом
from func import *

@bot.message_handler(content_types=["text"])
def text(message):
	print('!!!')
	try:
		chat, id, text = message.forward_from_chat.id, message.forward_from_message_id, message.text
	except:
		chat, id, text = message.chat.id, message.message_id, message.text

	with open('data/messages.txt', 'a') as file:
		print(json.dumps([chat, id, text], ensure_ascii=False), file=file)

if __name__ == '__main__':
	bot.polling(none_stop=True)