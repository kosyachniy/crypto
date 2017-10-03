from func import *

def add():
	@bot.message_handler(content_types=["text"])
	def text(message):
		print('!!!')
		try:
			chat, id, text = message.forward_from_chat.id, message.forward_from_message_id, message.text
			print('!4')
		except:
			chat, id = message.chat.id, message.message_id, message.text
			print('!5')

		with open('data/messages.txt', 'a') as file:
			print(json.dumps([chat, id, text]), file=file)
		print('!6')

	bot.polling(none_stop=True)

if __name__ == '__main__':
	add()