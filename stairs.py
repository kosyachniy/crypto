from func.trade import stock, bar

exc = 1
cur = 'eth'

y = stock[exc].last(cur)

m5 = bar(y, 5, 1) #2)
m1 = bar(y, 1, 1) #2)

m5 = m5[0][-1] - m5[0][0] #[m5[i][-1] - m5[i][0] for i in sorted(m5.keys())]
m1 = m1[0][-1] - m1[0][0] #[m1[i][-1] - m1[i][0] for i in sorted(m1.keys())]

#size1trend1 = m5[]

if m5 >= 0 and m1 > 0:
	print('In', stock[exc].price(cur, 'buy'))
	t = True

	while t:
		delay(1)
		

print(m5)
print(m1)
