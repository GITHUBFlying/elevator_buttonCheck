#!/usr/bin/python
# -*- coding: utf-8 -*
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt

#oimg =  cv2.cvtColor(ooimg, cv2.COLOR_BGR2GRAY)
oimg = cv2.imread('w2.png')
ooimg = cv2.imread('w2.png',0)


#cv2.imshow('oimg',oimg)
#cv2.imshow('oimg',oimg)

##9---滤波领域直径
#后面两个数字：空间高斯函数标准差，灰度值相似性标准差
imgrey= cv2.bilateralFilter(ooimg,9,200,200)
#中值模糊
#imgrey= cv2.medianBlur(oimg,25)
cv2.imshow('fimg',imgrey)

cv2.waitKey(0)
