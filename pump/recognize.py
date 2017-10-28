import pytesseract, cv2, sys
import numpy as np
from PIL import Image
import timeit

def recognize(src='1.jpg'):
	img = cv2.imread('re/' + src)
	cv2.imwrite('re/re.png', img)

	img = cv2.imread('re/re.png')
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	kernel = np.ones((1, 1), np.uint8)
	img = cv2.dilate(img, kernel, iterations=1)
	img = cv2.erode(img, kernel, iterations=1)
	cv2.imwrite('re/re.png', img)

	'''
	img = cv2.imread('re/re.png')
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	kernel = np.ones((1, 1), np.uint8)
	img = cv2.dilate(img, kernel, iterations=1)
	img = cv2.erode(img, kernel, iterations=1)
	cv2.imwrite('re/re.png', img)

	img = cv2.imread('re/re.png')
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	hsv[:,:,2] += 100
	img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
	cv2.imwrite('re/re.png', img)
	'''

	result = pytesseract.image_to_string(Image.open('re/re.png'))
	if result: return result

	img = cv2.imread('re/re.png')
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	img[:,:,2] = [[pixel + 500 if pixel < 200 else pixel - 500 for pixel in row] for row in img[:,:,2]]
	img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
	#img = cv2.bitwise_not(img)

	#a = timeit.default_timer()
	img = cv2.blur(img, (5, 5))
	#img = cv2.fastNlMeansDenoisingColored(img, None, 100, 100, 7, 21)
	#print(timeit.default_timer() - a)

	cv2.imwrite('re/re.png', img)

	result = pytesseract.image_to_string(Image.open('re/re.png'))
	return result

if __name__ == '__main__':
	print(recognize(sys.argv[1] if len(sys.argv) == 2 else '1.jpg'))