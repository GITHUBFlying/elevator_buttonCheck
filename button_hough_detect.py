#!/usr/bin/python
# -*- coding: utf-8 -*
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt

imgo=cv2.imread('t.png')
img=cv2.imread('t.png',0) #Input a picture

'''
kernel = np.ones((5,5),np.uint8)

#闭运算 先先膨胀在腐蚀 填充前景物体小洞
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# 中值滤波
#img = cv2.medianBlur(img,5)
#img=closing
#ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#11 为 Block size, 2 为 C
# Otsu's thresholding after Gaussian filtering
#(5,5)为高斯核的大小,0 为标准差
#blur = cv2.GaussianBlur(img,(3,3),0)
# 阈值一定要设为 0!
#ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# 中值滤波
img = cv2.medianBlur(img,5)
ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#11 为 Block size, 2 为 C 值
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
titles = ['Original Image', 'Global Thresholding (v = 127)',
'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]
for i in xrange(4):
	plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
	plt.title(titles[i])
	plt.xticks([]),plt.yticks([])

plt.show()
'''
#img = cv2.medianBlur(img,3)
#cv2.imshow('ori',img)
#img= cv2.bilateralFilter(img,9,75,75)
imgrey= cv2.medianBlur(img,25)
cv2.imshow('fimg',img)
#cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=40,minRadius=10,maxRadius=30)
#circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,50,param1=50,param2=20,minRadius=20,maxRadius=200)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
	# draw the outer circle
	cv2.circle(imgo,(i[0],i[1]),i[2],(0,255,0),2)
	# draw the center of the circle
	cv2.circle(imgo,(i[0],i[1]),2,(0,0,255),3)
cv2.imshow('detected circles',imgo)
cv2.waitKey(0)
