from func import *

#Данные
currencies = [
	['DigitalNote', 'XDN'],
	['Lunyr', 'LUN'],
	['CapriCoin', 'CPC'],
	['Ethereum', 'ETH'],
	['BitcoinCash', 'BCH'],
	['Litecoin', 'LTC'],
	['Dash', 'DASH'],
	['Zcash', 'ZEC'],
	['Ripple', 'XRP'],
	['OmiseGO', 'OMG'],
	['Monero', 'XMR'],
	['Dogecoin', 'DOGE'],
	['Dashcoin', 'DSH'],
	['NEO', 'NEO'],
	['BitShares', 'BTS'],
	['EthereumClassic', 'ETC'],
	['Clams', 'CLAM'],
	['Siacoin', 'SC'],
	['BelaCoin', 'BELA'],
	['NEM', 'XEM'],
	['DigiByte', 'DGB'],
	['Stratis', 'STRAT'],
	['Myriad-scrypt', 'MYR'],
	['Einsteinium', 'EMC2'],
	['Decred', 'DCR'],
	['NeosCoin', 'NEOS'],
	['MaidSafeCoin', 'MAID'],
	['Nexium', 'NXC'],
	['VertCoin', 'VTC'],
	['Factom', 'FCT'],
	['Syscoin', 'SYS'],
	['Nxt', 'NXT'],
	['Steemit', 'STEEM'],
	['lbryCoin', 'LBC'],
	['ByteCoin', 'BCN'],
	['Navcoin', 'NAV'],
	['FoldingCoin', 'FLDC'],
	['ViaCoin', 'VIA'],
	['Cloakcoin', 'CLOAK'],
	['Augur', 'REP'],
	['Counterparty', 'XCP'],
	['BURST', 'BURST'],
	['BitcoinPlus', 'XBC'],
	['BlackCoin', 'BLK'],
	['Expanse', 'EXP'],
	['Waves', 'WAVES'],
	['Potcoin', 'POT'],
	['BitcoinDark', 'BTCD'],
	['VeriCoin', 'VRC'],
	['PascalCoin', 'PASC'],
	['Florin', 'FLO'],
	['Peercoin', 'PPC'],
	['Primecoin', 'XPM'],
	['Radium', 'RADS'],
	['Iconomi', 'ICN'],
	['Vcash', 'XVC'],
	['BitCrystals', 'BCY'],
	['CureCoin', 'CURE'],
	['PinkCoin', 'PINK'],
	['Sibcoin', 'SIB'],
	['Voxels', 'VOX'],
	['Namecoin', 'NMC'],
	['EmerCoin', 'EMC'],
	['RieCoin', 'RIC'],
	['Gridcoin', 'GRC'],
	['DNotes', 'NOTE'],
	['Nautiluscoin', 'NAUT'],
	['Polybius', 'PLBT'],
	['Bata', 'BTA'],
	['HellenicCoin', 'HNC'],
	['ArcticCoin', 'ARC'],
	['Craftcoin', 'CRC'],
	['MonaCoin', 'MONA'],
	['Huntercoin', 'HUC'],
	['LEOcoin', 'LEO'],
	['BitSend', 'BSD'],
	['Bitmark', 'BTM'],
	['Transfercoin', 'TX'],
	['Novacoin', 'NVC'],
	['BlueCoin', 'BLU'],
	['Sexcoin', 'SXC'],
	['GroestlCoin', 'GRS'],
	['AdzCoin', 'ADZ'],
	['Solarcoin', 'SLR'],
	['EDinar', 'EDR'],
	['PostCoin', 'POST'],
	['ElCoin', 'EL'],
	['DrCoin', 'ISK'],
	['Fastcoin', 'FST'],
	['BitcoinUnlimited', 'BCU'],
	['Yocoin', 'YOC'],
	['UNCoin', 'UNC'],
	['CrevaCoin', 'CREVA'],
	['DaMaCoin', 'DMC'],
	['Leadcoin', 'LDC'],
	['PayPro', 'PRO'],
	['TrumpCoin', 'TRUMP'],
	['Dimecoin', 'DIME'],
	['10kCoin', '10K'],
	['1Credit', '1CR'],
	['2GiveCoin', '2GIVE'],
	['365coin', '365'],
	['IOTA', 'MIOTA'],
	['BitConnect', 'BCC'],
	['Lisk', 'LSK'],
	['Qtum', 'QTUM'],
	['Tether', 'USDT'],
	['Kyber Network', 'KNC'],
	['Ark', 'ARK'],
	['TenX', 'PAY'],
	['Gas', 'GAS'],
	['Golem', 'GNT'],
	['Basic Attention Token', 'BAT'],
	['Hshare', 'HSR'],
	['Stellar Lumens', 'XLM'],
	['Komodo', 'KMD'],
	['Metal', 'MTL'],
	['PIVX', 'PIVX'],
	['DigixDAO', 'DGD'],
	['Civic', 'CVC'],
	['Byteball Bytes', 'GBYTE'],
	['Ardor', 'ARDR'],
	['GameCredits', 'GAME'],
	['Populous', 'PPT'],
	['Nexus', 'NXS'],
	['MCAP', 'MCAP'],
	['SingularDTV', 'SNGLS'],
	['Bytom', 'BTM'],
	['Gnosis', 'GNO'],
	['0x', 'ZRX'],
	['Blocknet', 'BLOCK'],
	['FunFair', 'FUN'],
	['Bancor', 'BNT'],
	['Binance Coin', 'BNB'],
	['Lykke', 'LKK'],
	['Aeternity', 'AE'],
	['Monaco', 'MCO'],
	['GXShares', 'GXS'],
	['Status', 'SNT'],
	['Verge', 'XVG'],
	['Edgeless', 'EDG'],
	['Syscoin', 'SYS'],
	['FirstCoin', 'FRST']
]

transfers = [
	['BitCoin', 'BTC', 'Ƀ']
]
transfer = transfers[0][2]

exchanges = [
	['YObit'],
	['Bittrex'],
	['Poloniex']
]

vocabulary = {
	'buy': {'buy', 'купить', 'покупаем', 'докупаем', 'докупаемся'},
	'sell': {'sell', 'продать', 'продаём', 'продаем'}
}

on = lambda text, words: any([word in text for word in words])

def price(x):
	return [0.0000046, 0.00000062][x+1]

while True:
#Список сообщений
	x = []
	with db:
		for i in db.execute("SELECT * FROM lastmessage"):
			chat, id = i
			text = ''

			try:
				text = bot.forward_message(136563129, chat, id + 1).text
			except:
				try:
					text = bot.forward_message(136563129, chat, id + 2).text
				except:
					id = 0
				else:
					id += 2
			else:
				id += 1

			if id:
				if text: #изображения
					x.append([chat, id, text.lower()])
				db.execute("UPDATE lastmessage SET message=(?) WHERE id=(?)", (id, chat))
			
			sleep(1)

	print(x)
	for i in x:
		buy = 0
		exc = -1
		cur = -1
		count = 1.0
		rub = price(-1)

#Распознание сигнала
		i_buy = on(i[2], vocabulary['buy'])
		i_sell = on(i[2], vocabulary['sell'])
		if i_buy and i_sell: continue

		if i_buy:
			buy = 2
		elif i_sell:
			buy = 1
		else:
			buy = 0

		for j in range(len(exchanges)):
			if exchanges[j][0].lower() in i[2]:
				exc = j
				break

		t = 0
		for j in range(len(currencies)):
			if currencies[j][1].lower() in i[2] or currencies[j][0].lower() in i[2]:
				if t == 0:
					t = 1
				elif t == 1:
					t = 2
					break

				cur = j
		if t == 2: continue #

		total = 0
		with db:
			for i in db.execute("SELECT * FROM currencies WHERE changer=(?) and currency=-1", (exc,)):
				total = i[3]

		#убрать рассчёт доли при продаже

#Определение количества
		operation = price(cur)
		delta = total * 0.03
		count = delta / operation

#Сборка сообщения на Telegram-канал
		if buy == 2:
			sign = '-'
		elif buy == 1:
			sign = '+'
		else:
			sign = '±'

		if buy == 2:
			buy = 'купить'
		elif buy == 1:
			buy = 'продать'
		else:
			buy = 'не определено'

		if cur == -1:
			cur1 = 'Криптовалюта не определена'
			cur2 = 'Индекс не определён'
		else:
			cur1 = currencies[cur][0]
			cur2 = currencies[cur][1]

		#постваить процент, после которого сделка совершится
		#проверка хватает ли денег
		bot.send_message(136563129, '%s (%s)\n%s - %s\n--------------------\n∑ %f%s (%d₽)\nK %f\nΔ %s%f%s (%s%d₽)' % (cur1, buy, exchanges[exc][0], cur2, total, transfer, total / rub, count, sign, delta, transfer, sign, delta / rub)) #T %d.%d %d:%d , day, month, hour, minute #-1001124440739 #бота перенести в отдельный файл
		bot.forward_message(136563129, chat, id + 2) #
		#запись в базу данных

		sleep(5)