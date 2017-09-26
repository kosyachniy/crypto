from func import *

url='https://ru.investing.com/crypto/currencies'

with open('../data/currencies.txt', 'w') as file:
	page = requests.get(url, headers={"User-agent": "Mozilla/5.0"}).text
	soup = BeautifulSoup(page, 'lxml')
	table = soup.find('table', id='top_crypto_tbl')
	tr = table.find_all('tr')
	for i in tr[1:]:
		td = i.find_all('td')

		name = td[1].text
		index = td[2].text
		price = td[3].text.replace('.', '')
		print(name, index, price)
		
		a = json.dumps([name, index])
		print(a, file=file)