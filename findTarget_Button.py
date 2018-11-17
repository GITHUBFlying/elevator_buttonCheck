#!/usr/bin/python
# -*- coding: utf-8 -*
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt

global BoundList
BoundList=[]
def addBound(rect):
	global BoundList
	leng=len(BoundList)
	flag=True
	if(leng is 0):
		BoundList.append(rect)
		return 
	else:
		for i in range(leng):
			ox=float(BoundList[i][0]+BoundList[i][2])/2
			oy=float(BoundList[i][1]+BoundList[i][3])/2
			cx=float(rect[0]+rect[2])/2
			cy=float(rect[1]+rect[3])/2
			if (abs(ox-cx)<20) and (abs(oy-cy)<20):
				oarea=BoundList[i][2]*BoundList[i][3]
				carea=rect[2]*rect[3]
				if carea<oarea:
					BoundList[i]=rect
					flag=False
					return
	if flag:
		BoundList.append(rect)
			

oimg = cv2.imread('r.png')
ooimg = cv2.imread('r.png',0)
#直方图均衡化　增强对比度# 试了几次不需要均衡化
#ooimg = cv2.equalizeHist(ooimg)

imgrey= cv2.bilateralFilter(ooimg,9,75,75)
BINARY_img = cv2.adaptiveThreshold(imgrey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

kernel = np.ones((1,1),np.uint8)
#膨胀 前景有一个是1 就是1 增加白色区域范围
erosion = cv2.dilate(BINARY_img,kernel,iterations = 1)
#膨胀腐蚀
#erosion = cv2.erode(BINARY_img,kernel,iterations = 1)

ero=cv2.resize(erosion,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)
contours,hierarchy=cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cLen=len(contours)
for i in range(0,cLen):
	rect= cv2.boundingRect(contours[i])
	x=rect[0]
	y=rect[1]
	w=rect[2]
	h=rect[3]
	aspect_ratio = float(w)/h
	
	#判断按键与数字
	if  ((aspect_ratio>0.5) and (aspect_ratio<1.3) ) or ((aspect_ratio<0.5) and(aspect_ratio>0.3)):
		rectArea=w*h
		if (rectArea>500) and (rectArea < 15000): 
			#挑选结果
			addBound(rect)
			#mg = cv2.rectangle(oimg,(x,y),(x+w,y+h),(255,0,0),2)
imgArray=[]
for i in range(len(BoundList)):
	x=BoundList[i][0]
	y=BoundList[i][1]
	w=BoundList[i][2]
	h=BoundList[i][3]
	#在原图像上画出该切割后的矩形框
	img = cv2.rectangle(oimg,(x,y),(x+w,y+h),(0,255,0),2)
	#
	#高和宽　切割图像
	img = cv2.rectangle(oimg,(x,y),(x+w,y+h),(0,255,0),2)
	sp=oimg.shape
	imgH=sp[0]
	imgW=sp[1]
	if y-5>0 and x-5>0 and y+h+5<imgH and x+w+5<imgW:
		cropImg=ooimg[(y-5):(y+h+5),(x-5):(x+w+5)]
	else:
		cropImg=ooimg[(y):(y+h),(x):(x+w)]
	ret,BINARY_img = cv2.threshold(cropImg,100,255,cv2.THRESH_BINARY)
	#缩放到30*40 宽和高
	resized=cv2.resize(BINARY_img, (30,35), interpolation=cv2.INTER_CUBIC)
	
	
	
	kernel = np.ones((2,2),np.uint8)
	#腐蚀
	#result = cv2.erode(resized,kernel,iterations = 1)
	#将图像腐蚀一波 在膨胀 即开运算 滤除背景白色噪声点
	result = cv2.morphologyEx(resized, cv2.MORPH_OPEN, kernel)
	imgArray.append(result)
'''
for i in range(len(imgArray)):
	cv2.imwrite("samples/"+str(i)+".png",imgArray[i])
	plt.subplot(5,5,i+1)
	plt.imshow(imgArray[i],'gray')
plt.show()
'''
res=cv2.resize(oimg,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)

cv2.imshow('img',res)
cv2.waitKey(0)
