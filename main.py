#from func.telegram import *
from pump import *
#from recognize import recognize

@bot.message_handler(content_types=["text"])
def text(message):
	pump(message.chat.id, message.text)

if __name__ == '__main__':
	bot.polling(none_stop=True)

'''
def autoadd():
	while True:
		t = False
		for i in range(1, 6):
			try:
				text = bot.forward_message(meid, chat, id + i) #.document.file_id #.text
			except:
				continue
			else:
				id = id + i
				t = True
				break

		if t:
			print(text)
			\'\'\'
			file_info = bot.get_file(message.document.file_id)
			downloaded_file = bot.download_file(file_info.file_path)
			pump(recognize())
			\'\'\'

if __name__ == '__main__':
	autoadd()
'''