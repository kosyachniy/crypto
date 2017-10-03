from func import *

@bot.message_handler(content_types=["text"])
def text(message):
	try:
		chat, id, text = message.forward_from_chat.id, message.forward_from_message_id, message.text
	except:
		chat, id = message.chat.id, message.message_id, message.text

	with open('data/messages.txt', 'a') as file:
		print(json.dumps([chat, id, text]), file=file)

if __name__ == '__main__':
	bot.polling(none_stop=True)