import cv2
import numpy as np
import time
def find_color(image):
	#Lower=np.array([0,0,0])
	#Upper=np.array([135,135,135])
	Lower=np.array([50,50,50])
	Upper=np.array([255,255,255])
	image_mask = cv2.inRange(image,Lower,Upper)
	result_image = cv2.bitwise_not(image,image,mask = image_mask)
	
	return result_image

def detect_Edge_area(image):
	image_Edge,contours,hierarchy = cv2.findContours(image,1,2)
	cnt = contours[0]
	area = cv2.contourArea(cnt)
	print("面積:",area)
	return area

def detect_Edge(image):
	imgEdge,contours,hierarchy = cv2.findContours(image, 1, 2)
	cnt = contours[0]
	#モーメント取得
	m = cv2.moments(cnt)
	#モーメントの重心算出
	cx = int(m["m10"]//m["m00"])
	cy = int(m["m01"]//m["m00"])
	#モーメントの重心を描画
	cv2.drawMarker(image,(cx,cy),color=(256,0,0))
	#モーメントの面積を算出
	area = cv2.contourArea(cnt)
	print("面積:",area)
	return image,area


def binarization(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	ret,th = cv2.threshold(gray,t,255,cv2.THRESH_BINARY)
	return gray,ret,th

def closing(image,kernel_size):
	#カーネルサイズ１００×１００
	kernel = np.ones((kernel_size,kernel_size,),np.uint8)
	#クロージング処理
	#膨張
	dilate = cv2.dilate(image,kernel)

	kernel = kernel-10
	kernel = np.ones((kernel_size,kernel_size,),np.uint8)
	#収縮
	erode = cv2.erode(dilate,kernel)
	
	return dilate,erode

	
def Main(image,t):
	print("入力画像サイズ:",image.shape)
	image_cope = image
	cv2.imshow("Orignal_image",image_cope)
	image = find_color(image)
	image_cut = image[110:290,220:500,:]
	image_resize = cv2.resize(image_cut,(1000,1000))

	gray,ret,th = binarization(image_resize)

	dilate,erode = closing(th,100)

	#エッジ検出
	canny_image = cv2.Canny(erode,50,110)
	
	canny_image,area = detect_Edge(canny_image)

	
	cv2.imshow("find_color",image)
	cv2.imshow("Binarization",th)
	cv2.imshow("dilate",dilate)
	cv2.imshow("erode",erode)
	cv2.imshow("Canny",canny_image)
	cv2.waitKey(0)



if __name__=="__main__":
	# 閾値
	t = 135
	image = cv2.imread("test2.jpg")
	Main(image,t)