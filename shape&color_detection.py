import cv2
import numpy as np

img = cv2.imread('Data1/pic11.png')

cnt_re = 0
cnt_ye = 0
cnt_gr = 0
i = 0
cnt_tri = 0 
cnt_squ = 0 
cnt_rec = 0
cnt_cir = 0

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY) # phân vùng
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
	if i == 0:
		i = 1
		continue
	approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
	cv2.drawContours(img, [contour], 0, (0,255,0), 5)
	M = cv2.moments(contour)
	x = int(M['m10']/M['m00'])
	y = int(M['m01']/M['m00'])
	pi = hsv_img[y][x]
	c = pi[0]
	if len(approx) == 3:
		cv2.putText(img, 'Triangle', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
		cnt_tri += 1
	elif len(approx) == 4:
		rect = cv2.minAreaRect(contour)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		tmp = cv2.norm(box[0], box[1])/ cv2.norm(box[0], box[-1])
		esp = 1e-2
		if (1 - esp < tmp < 1 + esp):
			cv2.putText(img, 'Square', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
			cnt_squ += 1
		else:
			cv2.putText(img, 'Rectangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
			cnt_rec += 1
	else:
		cv2.putText(img, 'circle', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
		cnt_cir += 1
	if c >= 160 and c <=180:
		name_color = "Red"
		cnt_re+=1
		cv2.putText(img, name_color, (x- 40, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
	elif c >= 15 and c <= 35:
		name_color = "Yellow"
		cnt_ye+=1
		cv2.putText(img, name_color, (x- 40, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
	elif c >= 40 and c <= 90:
		name_color = "Green"
		cnt_gr+=1
		cv2.putText(img, name_color, (x- 40, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)

print("Kết quả")
print("+ Có " + str(cnt_cir) + " hình tròn, " + str(cnt_tri) + " hình tam giác, "+ str(cnt_rec) + " hình chữ nhật, " + str(cnt_squ) + " hình vuông.")
cv2.imshow('shapes', img)
print("+ Màu đỏ:", str(cnt_re) + " hình")
print("+ Màu xanh:", str(cnt_gr) + " hình")
print("+ Màu vàng:", str(cnt_ye) + " hình")
cv2.waitKey(0)
cv2.destroyAllWindows()
