import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('Data/pic1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
#cv2.imshow('shape', gray)
#cv2.imshow('shape1', threshold)

contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#print(len(contours))

i = 0
cnt_tri = 0 
cnt_squ = 0 
cnt_rec = 0
cnt_cir = 0

for contour in contours:
	if i == 0:
		i = 1
		continue
	approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
	cv2.drawContours(img, [contour], 0, (0,255,0), 5)
	M = cv2.moments(contour)
	if M['m00'] != 0.0:
		x = int(M['m10']/M['m00'])
		y = int(M['m01']/M['m00'])
	if len(approx) == 3:
		cv2.putText(img, 'Triangle', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
		cnt_tri += 1
	elif len(approx) == 4:
		x1, y1, w, h = cv2.boundingRect(contour)
		if  ((float(w)/h)==1):
			cv2.putText(img, 'Square', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
			cnt_squ += 1
		else:
			cv2.putText(img, 'Rectangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
			cnt_rec += 1
	else:
		cv2.putText(img, 'circle', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
		cnt_cir += 1
print("Kết quả")
print("+ Có " + str(cnt_cir) + " hình tròn, " + str(cnt_tri) + " hình tam giác, "+ str(cnt_rec) + " hình chữ nhật, " + str(cnt_squ) + " hình vuông.")
cv2.imshow('shapes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
