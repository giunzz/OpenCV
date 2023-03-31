import cv2
import numpy as np

img = cv2.imread('Data1/shape.png')

def calculate_mask(lower_color, upper_color, hsv_img):
    kernal = np.ones((5, 5), "uint8")
    color_lower = np.array(lower_color, np.uint8)
    color_upper = np.array(upper_color, np.uint8)
    color_mask = cv2.inRange(hsv_img, color_lower, color_upper)
    color_mask = cv2.dilate(color_mask, kernal)
    return color_mask

def detect_specific_color(color_mask, name_color, img):
    contours,_ = cv2.findContours(color_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt = len(contours)
    if( name_color == "Red"):  print("+ Màu đỏ:", str(cnt) + " hình")
    if( name_color == "Green"):  print("+ Màu xanh lá:", str(cnt)+ " hình")
    if( name_color == "Yellow"):  print("+ Màu vàng:", str(cnt) + " hình")
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            cv2.putText(img, name_color, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
def detect_color(img):
    detect_specific_color(calculate_mask([136, 87, 111], [180, 255, 255],  hsv_img), "Red", img)
    detect_specific_color(calculate_mask([40, 40, 40], [70, 255, 255],  hsv_img), "Green", img)
    detect_specific_color(calculate_mask([20, 100, 100], [30, 255, 255],  hsv_img), "Yellow", img)
    return img

i = 0
cnt_tri = 0 
cnt_squ = 0 
cnt_rec = 0
cnt_cir = 0

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY) # phân vùng
cv2.imshow('r', threshold)
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
	k = hsv_img[x][y]
	if len(approx) == 3:
		cv2.putText(img, 'Triangle', (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0), 2)
		cnt_tri += 1
	elif len(approx) == 4:
		rect = cv2.minAreaRect(contour)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		tmp = cv2.norm(box[0], box[1])/ cv2.norm(box[0], box[-1])
		print(tmp)
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

print("Kết quả")
print("+ Có " + str(cnt_cir) + " hình tròn, " + str(cnt_tri) + " hình tam giác, "+ str(cnt_rec) + " hình chữ nhật, " + str(cnt_squ) + " hình vuông.")
detect_color(img)
cv2.imshow('shapes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
