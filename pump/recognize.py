import pytesseract, cv2, sys
import numpy as np
from PIL import Image

def recognize(src = '1.jpg'):
	'''
	img = cv2.imread('re/' + src, 0)
	rows, cols = img.shape
	M = np.float32([[1, rows * 0.8, cols * 0.8], [0, rows * 0.2, cols * 0.2]])
	img = cv2.warpAffine(img, M, (cols, rows))
	cv2.imwrite('re/-' + src, img)
	'''

	'''
	img = Image.open('re/' + src)
	width = img.size[0]
	height = img.size[1]
	img = img.crop((width * 0.8, height * 0.8, width, height))
	'''

	img = Image.open('re/' + src).convert('L')
	width, height = img.size[0], img.size[1]
	img = img.crop((int(width * 0.8), int(height * 0.85), width, height))
	img.save('re/-' + src)

	img = cv2.imread('re/-' + src)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	kernel = np.ones((1, 1), np.uint8)
	img = cv2.dilate(img, kernel, iterations=1)
	img = cv2.erode(img, kernel, iterations=1)

	#cv2.rectangle(img, (100, 100), (300, 300), (0, 0, 255), 3)

	#cv2.imwrite('re/re.png', img)
	#img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	cv2.imwrite('re/thres.png', img)
	result = pytesseract.image_to_string(Image.open('re/thres.png'))

	return result

if __name__ == '__main__':
	print(recognize(sys.argv[1] if len(sys.argv) == 2 else '1.jpg'))