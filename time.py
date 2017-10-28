import pytesseract, cv2, sys
import numpy as np
from PIL import Image

def recognize(src = '1.jpg'):
	img = Image.open('re/' + src).convert('L')
	width, height = img.size[0], img.size[1]
	img = img.crop((int(width * 0.8), int(height * 0.85), width, height))
	img.save('re/-' + src)

	img = cv2.imread('re/-' + src)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	kernel = np.ones((1, 1), np.uint8)
	img = cv2.dilate(img, kernel, iterations=1)
	img = cv2.erode(img, kernel, iterations=1)

	cv2.imwrite('re/thres.png', img)
	result = pytesseract.image_to_string(Image.open('re/thres.png'))

	return [i for i in result.split() if ':' in i][0]

if __name__ == '__main__':
	print(recognize(sys.argv[1] if len(sys.argv) == 2 else '1.jpg'))