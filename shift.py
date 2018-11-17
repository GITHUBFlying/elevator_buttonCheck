#!/usr/bin/python
# -*- coding: utf-8 -*
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('w2.png')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sift = cv2.SIFT()
kp = sift.detect(gray,None)
img=cv2.drawKeypoints(gray,kp)

cv2.imshow("res",img)
cv2.waitKey(0)
