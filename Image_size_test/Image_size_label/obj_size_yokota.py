import cv2
import numpy as np
import pprint

#影を除去する関数
def Remove_shadow(img,ksize):
	
	blur = cv2.blur(img,(ksize,ksize))
	rij = img/blur
	# 1以上の値を除外
	index_1 = np.where(rij >= 1.00) 
	rij[index_1] = 1
	# 除算結果が実数値になるため整数に変換
	rij_int = np.array(rij*255, np.uint8)
	rij_HSV = cv2.cvtColor(rij_int, cv2.COLOR_BGR2HSV)
	ret, thresh = cv2.threshold(rij_HSV[:,:,2], 0, 255, cv2.THRESH_OTSU)
	rij_HSV[:,:,2] = thresh
	rij_ret = cv2.cvtColor(rij_HSV, cv2.COLOR_HSV2BGR)
	return rij_ret


def find_color(image):
	#Lower=np.array([0,0,0])
	#Upper=np.array([135,135,135])
	Lower=np.array([135,135,135])
	Upper=np.array([255,255,255])
	image_mask = cv2.inRange(image,Lower,Upper)
	result_image = cv2.bitwise_not(image,image,mask = image_mask)
	
	return result_image




def Main():
	# 閾値
	t = 135
	ksize = 55
	#入力画像
	image = cv2.imread("test5.jpg")
	print(image.shape)
	image_copy = image
	image = image[100:300,220:500,:]
	print(image.shape)
	#image = find_color(image)
	image = cv2.resize(image,(1000,1000))


	rij_ret = Remove_shadow(image,ksize)
	#2値化
	gray = cv2.cvtColor(rij_ret,cv2.COLOR_BGR2GRAY)
	ret,th = cv2.threshold(gray,t,255,cv2.THRESH_BINARY)


	#rij_ret = Remove_shadow(image,ksize)
	##2値化
	#gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#ret,th = cv2.threshold(gray,t,255,cv2.THRESH_BINARY)

	kernel = np.ones((6,6,),np.uint8)

	dilate = cv2.dilate(gray,kernel)
	erode = cv2.erode(dilate,kernel)
	erode = cv2.bitwise_not(erode)
	#erode = cv2.erode(gray,kernel)

	black = 0
	white = 255
	#for i in erode:
	#	for j in i:
	#		if


	erode[np.where((erode == white))] = black
	#エッジ抽出
	canny_image = cv2.Canny(erode,50,110)


	##輪郭線検出
	#imgEdge,contours,hierarchy = cv2.findContours(canny_image, 1, 2)
	#cnt = contours[0]
	##モーメント取得
	#m = cv2.moments(cnt)
	##モーメントの重心算出
	#cx = int(m["m10"]//m["m00"])
	#cy = int(m["m01"]//m["m00"])
	##モーメントの重心を描画
	#cv2.drawMarker(canny_image,(cx,cy),color=(256,0,0))
	##モーメントの面積を算出
	#area = cv2.contourArea(cnt)
	#print("面積:",area)


	cv2.imshow("ORIGNAL",image)
	cv2.imshow("result",rij_ret)
	cv2.imshow("Binarization",gray)
	cv2.imshow("dilate",dilate)
	cv2.imshow("erode",erode)
	cv2.imshow("Canny",canny_image)
	cv2.waitKey(0)



if __name__=="__main__":
	Main()
