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
			#ow=BoundList[i][2]
			#cw=rect[2]
			#oy=BoundList[i][2]
			#cy=rect[3]
			if (abs(ox-cx)<20) and (abs(oy-cy)<20):
				print 't'
				print ox,cx,oy,cy
				print ox-cx
				print oy-cy
				oarea=BoundList[i][2]*BoundList[i][3]
				carea=rect[2]*rect[3]
				#取较大的面积
				if carea<oarea:
					BoundList[i]=rect
					flag=False
					return
	if flag:
		BoundList.append(rect)
			

#oimg =  cv2.cvtColor(ooimg, cv2.COLOR_BGR2GRAY)
oimg = cv2.imread('k.png')
ooimg = cv2.imread('k.png',0)


#cv2.imshow('oimg',oimg)
#cv2.imshow('oimg',oimg)

##9---滤波领域直径
#后面两个数字：空间高斯函数标准差，灰度值相似性标准差
imgrey= cv2.bilateralFilter(ooimg,9,75,75)
#中值模糊
#imgrey= cv2.medianBlur(oimg,25)
#cv2.imshow('fimg',imgrey)
#cv2.imshow('grey_img',imgray)
BINARY_img = cv2.adaptiveThreshold(imgrey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
#ret,BINARY_img = cv2.threshold(imgrey,100,255,cv2.THRESH_BINARY)
#cv2.imshow('BINARY_img',BINARY_img)

kernel = np.ones((1,1),np.uint8)
#膨胀 前景有一个是1 就是1 增加白色区域范围
erosion = cv2.dilate(BINARY_img,kernel,iterations = 1)
#膨胀腐蚀
#erosion = cv2.erode(BINARY_img,kernel,iterations = 1)

ero=cv2.resize(erosion,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)
cv2.imshow('dilate',ero)
#cv2.waitKey(0)
'''
第一个参数是寻找轮廓的图像；

第二个参数表示轮廓的检索模式，有四种（本文介绍的都是新的cv2接口）：
    cv2.RETR_EXTERNAL 表示只检测外轮廓
    cv2.RETR_LIST检 测的轮廓不建立等级关系
    cv2.RETR_CCOMP 建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
    cv2.RETR_TREE 建立一个等级树结构的轮廓。

第三个参数method为轮廓的近似办法
    cv2.CHAIN_APPROX_NONE  存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），abs（y2-y1））==1
    cv2.CHAIN_APPROX_SIMPLE 压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
    cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh-Chinl chain 近似算法
'''

contours,hierarchy=cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#print cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cLen=len(contours)
for i in range(0,cLen):
	#epsilon = 0.1*cv2.arcLength(contours[i],True)
	#approx = cv2.approxPolyDP(contours[i],epsilon,True)
	#mC.append(approx)
	#cv2.drawContours(rgbimg, mC, -1, (0,0,255), 3)
	rect= cv2.boundingRect(contours[i])
	#x,y,w,h = cv2.boundingRect(contours[i])
	x=rect[0]
	y=rect[1]
	w=rect[2]
	h=rect[3]
	aspect_ratio = float(w)/h
	
	#判断按键与数字
	if  ((aspect_ratio>0.5) and (aspect_ratio<1.3) ) or ((aspect_ratio<0.5) and(aspect_ratio>0.3)):
		#if  aspect_ratio>0.6:
		#epsilon = 0.1*cv2.arcLength(contours[i],True)
		#approx = cv2.approxPolyDP(contours[i],epsilon,True)
		#cv2.drawContours(rgbimg, approx, -1, (0,0,255), 3)
		#cv2.drawContours(oimg, contours, i, (0,0,255), 3)
		#area = cv2.contourArea(contours[i])
		rectArea=w*h
		if (rectArea>500) and (rectArea < 15000): 
			#cv2.drawContours(oimg, contours, i, (0,0,255), 3)
			#	print 'counting area %d\n'%area
			#print 'rect area %d\n'%(w*h)
			addBound(rect)
			#cv2.drawContours(ooimg, contours, i, (0,0,255), 3)
			#epsilon = 0.1*cv2.arcLength(contours[i],True)
			#approx = cv2.approxPolyDP(contours[i],epsilon,True)
			#img = cv2.rectangle(oimg,(x,y),(x+w,y+h),(255,0,0),2)
			#print approx
			#cv2.rectangle(ooimg,approx[0],approx[2],(0,255,0),1)'''
for i in range(len(BoundList)):
	x=BoundList[i][0]
	y=BoundList[i][1]
	w=BoundList[i][2]
	h=BoundList[i][3]
	#print "x is %f"%(float(x+w)/2)
	#print  "y is %f"%(float(y+h)/2)
	img = cv2.rectangle(oimg,(x,y),(x+w,y+h),(0,255,0),2)
	cropImg=ooimg[(y-10):(y+h+10),(x-10):(x+w+10)]
	ret,BINARY_img = cv2.threshold(cropImg,100,255,cv2.THRESH_BINARY)
	cv2.imshow('wsef'+str(i),BINARY_img)
res=cv2.resize(oimg,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)
cv2.imshow('img',res)
#print 'Boudlist'
#print BoundList
cv2.waitKey(0)
