#!/usr/bin/python
# -*- coding: utf-8 -*
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt


oimg = cv2.imread('w2.png')
ooimg = cv2.imread('w2.png',0)
print ooimg.shape
cv2.imshow("oimg",ooimg)
equ = cv2.equalizeHist(ooimg)

cv2.imshow("res",equ)
cv2.waitKey(0)
