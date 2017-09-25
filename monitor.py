from time import sleep

def monitor(x):
	while True:
		#x['trade'].append([1, 0.01, 25, 9, 15, 10])
		x.append([0, 1, 2, 3, 4])
		sleep(2)
		print(x)