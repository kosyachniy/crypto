from func import *

while True:
	delta, day, month, hour, minute = 0.01, 25, 9, 15, 10

	if delta >= 0.01: #постваить процент, после которого сделка совершится
		bot.send_message(136563129, 'BitCoin\n----------\nΔ +%.2f$\nT %d.%d %d:%d' % (delta, day, month, hour, minute)) #-1001124440739 #бота перенести в отдельный файл
		#запись в базу данных

	sleep(5)