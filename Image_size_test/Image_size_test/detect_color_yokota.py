import cv2
import numpy as np
import time
def find_color(image):
	#Lower=np.array([0,0,0])
	#Upper=np.array([135,135,135])
	Lower=np.array([135,135,135])
	Upper=np.array([255,255,255])
	image_mask = cv2.inRange(image,Lower,Upper)
	result_image = cv2.bitwise_not(image,image,mask = image_mask)
	
	return result_image

def Main(image,t):
	print("入力画像サイズ:",image.shape)
	image_cope = image

	image = find_color(image)
	cv2.imshow("find_color",image)
	cv2.waitKey(0)
	

	time.sleep(5)


if __name__=="__main__":
	# 閾値
	t = 135
	image = cv2.imread("test2.jpg")
	Main(image,t)