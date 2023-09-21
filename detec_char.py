import cv2
import numpy as np

#Màu đỏ: 
lower_red = np.array([160,100,100]) 
upper_red = np.array([180,255,255]) 

#Màu vàng: 
lower_yellow = np.array([15,150,150]) 
upper_yellow = np.array([35,255,255]) 

#Màu xanh:
lower_green = np.array([40,50,50]) 
upper_green = np.array([90,255,255])

#đọc ảnh
img = cv2.imread("Data1/shape.png")

#cv2.inRange(ảnh,dải màu thấp,dải màu cao)

#lọc ảnh có màu đỏ
#r = cv2.inRange(hsv,lower_red,upper_red)
#cv2.imshow('rimg',r)

#lọc ảnh có màu vàng
#y = cv2.inRange(hsv,lower_yellow,upper_yellow)
#cv2.imshow('yimg',y)

#lọc ảnh có màu xanh
#g = cv2.inRange(hsv,lower_green,upper_green)
#cv2.imshow('gimg',g)

#tri,rec,sqr,cir: các biến đếm số lượng hình tam giác, hình chữ nhật, hình vuông, hình tròn
tri,rec,sqr,cir=0,0,0,0
#xác định hình dạng của từng hình
def shape_detect(c):
    global tri,rec,sqr,cir
    # khởi tạo tên của hình và kích thước xấp xỉ của đường viền(contours)
    shape = "unidentified" 
    peri = cv2.arcLength(c, True) # tính chu vi (perimeter) của đường viền
    approx = cv2.approxPolyDP(c, 0.04 * peri, True) # tính kích thước xấp xỉ
    # nếu là hình tam giác thì nó có ba đỉnh
    if len(approx) == 3:
        shape = "triangle"
        tri+=1
    # nếu là hình có bốn đỉnh thì nó có thể là hình chữ nhật hoặc hình vuông
    elif len(approx) == 4:
	# Tính toán khung giới hạn của đường viền và sử dụng các điểm thuộc khung đó để tính tỷ lệ khung hình
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
	# hình vuông sẽ có tỉ lệ khung hình(aspect ratio) xấp xỉ nhau 
	# nếu tỉ lệ bằng 1 thì là hình vuông còn lại là hình chữ nhật
        if ar == 1:
            shape = "square"
            sqr+=1
        else:
            shape = "rectangle"
            rec+=1
    # còn lại sẽ là các hình tròn
    else:
        shape = "circle"
        cir+=1
    # trả về tên của hình
    return shape

#re,ye,gr: các biến đếm hình màu đỏ, màu vàng, màu xanh
re,ye,gr=0,0,0
#xác định màu của từng hình
def color_detect(hue):
    global re,ye,gr
    color = "unidentified"
    # nếu giá trị hue của điểm pixel từ 160 đến 180 là màu đỏ
    if hue >= 160 and hue <=180:
        color = "red"
        re+=1
    # nếu giá trị hue của điểm pixel từ 15 đến 35 là màu vàng
    elif hue >= 15 and hue <= 35:
        color = "yellow"
        ye+=1
    # nếu giá trị hue của điểm pixel từ 40 đến 90 là màu xanh
    elif hue >= 40 and hue <=90:
        color = "green"
        gr+=1
    return color

#chuyển ảnh từ hệ màu BGR sang xám
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#chuyển từ hệ màu BGR sang hệ màu HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#tách ngưỡng
_,threshold = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
#xác định đường viền
contours,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

i = 0
for c in contours:
    #khi xác định đường viền sẽ có đường viền của khung ảnh nên loại bỏ đường viền đó
    if i == 0:
        i = 1
        continue
    #xác định điểm trọng tâm của đường viền
    M = cv2.moments(c) #hàm cv2.moments(): nêu các đặc trưng của đường viền c
    if M["m00"] != {0,0}:
        cX = int(M["m10"] / M["m00"]) # tọa độ x của điểm trọng tâm đường viền 
        cY = int(M["m01"] / M["m00"]) # tọa độ y của điểm trọng tâm đường viền
        #lấy pixel của điểm trọng tâm đường viền trên ảnh có hệ màu HSV
        pixel=hsv[cY, cX]
        #lấy chỉ số hue trong hệ màu HSV
        hue=pixel[0]
        shape = shape_detect(c)
        color = color_detect(hue)
        
        #ghi tên kiểu hình lên điểm trọng tâm của đường viền 
        cv2.putText(img, shape, (cX-20, cY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        #ghi tên kiểu hình lên điểm trọng tâm của đường viền 
        cv2.putText(img, color, (cX-20, cY+10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
#triangle,rectangle,square,circle:hình tam giác, hình chữ nhật, hình vuông, hình tròn
#red,yellow,green:màu đỏ,màu vàng,màu xanh  

#ghi số lượng mỗi loại hình có trong ảnh
print("Có " + str(tri) + " hình tam giác,", str(rec) + " hình chữ nhật,", str(sqr) + " hình vuông,", str(cir) + " hình tròn")
#ghi số lượng các hình cùng màu
print("Có " + str(re) + " màu đỏ,", str(ye) + " màu vàng,", str(gr) + " màu xanh")

cv2.imshow("Image", img)
cv2.waitKey()
cv2.destroyAllwindows()
