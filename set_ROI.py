#! /usr/bin/env python
# -*- coding:utf-8 -*-
# 从图像中截图
import cv2
import numpy as np
# 先进行初始化
RED = [0, 0, 255]
rect = (0, 0, 1, 1)
drawing = False
rectangle = False
rect_over = False
rect_or_mask = 100
thickness = 2

def rectangle_roi(event, x, y, flags, param):
    global img, img2, dst, drawing, mask, rectangle, rect, rect_or_mask, ix, iy, rect_over

    # Draw Rectangle
    if event == cv2.EVENT_RBUTTONDOWN:
        rectangle = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle == True:
            img = img2.copy()
            cv2.rectangle(img, (ix, iy), (x, y), RED, thickness)
            rect = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))
            rect_or_mask = 0

    elif event == cv2.EVENT_RBUTTONUP:
        rectangle = False
        rect_over = True
        cv2.rectangle(img, (ix, iy), (x, y), RED, thickness)
        rect = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))
        rect_or_mask = 0
        print(" Now press the key 'n' a few times until no further change \n")


if __name__ == "__main__":
    filename = "a.png"
    img = cv2.imread(filename)
    img2 = img.copy()
    cv2.namedWindow('input')
    cv2.setMouseCallback('input', rectangle_roi)

    print(" Draw a rectangle around the object using right mouse button \n")
    while(1):
        cv2.imshow('input',img)
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k == ord('r'):
            print("resetting \n")
            rect = (0, 0, 1, 1)
            drawing = False
            rectangle = False
            rect_or_mask = 100
            rect_over = False
            img = img2.copy()
        elif k == ord('n'):
            if (rect_or_mask == 0):
                x1, y1, x2, y2 = rect
                # print rect
                dst = img[(y1+2):(y1+y2-2), (x1+2):(x1+x2-2)]
                cv2.imshow("dst", dst)
                cv2.waitKey(0)
        elif k == ord("s"):
            x1, y1, x2, y2 = rect
            dst = img[(y1 + 2):(y1 + y2 - 2), (x1 + 2):(x1 + x2 - 2)]
            roi_title = "ROI_" + filename
            cv2.imwrite(roi_title, dst)

    cv2.destroyAllWindows()
