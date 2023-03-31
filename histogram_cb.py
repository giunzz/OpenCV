#histogram của 1 cảnh là tần suất xuất hiện của các mức xám
#cân bằng histogram
#   + Thực hiện khi cảnh quá tối / sáng
#   + Bước tiền xử lý ảnh
# b1 : Tính tần suất mức xám của ảnh
# b2 : Tính new_pi = (l + pi)/ (w*h) 
#         l : max(img), w*h : kích thước của cảnh
# b3 : cộng dồn 
#         new_pi = tong new_pi(1 -> i) 
# b4 : lam tron 
#         new_pi = round(new_pi)
# b5 : anh xa 
#         img[i][j] = p[img[i][j]]lênh
import cv2
import numpy as np
from matplotlib import pyplot as plt

def cal_h(img):
    maxg = np.max(img)
    w,h = img.shape
    p = [0] * (maxg + 1)
    for i in range(w):
        for j in range(h): p[img[i][j]] += 1
    return p

img = cv2.imread("b.jpg", cv2.IMREAD_GRAYSCALE)
w,h = img.shape
L = np.max(img)
p =[0] * (L + 1)
for i in range(w):
        for j in range(h): p[img[i][j]] += 1
for i in range(L + 1) : p[i] = L * p[i] / (w * h)
for i in range(1,L + 1) : p[i] = p[i - 1] + p[i]
for i in range(1,L + 1) : p[i] = round(p[i])
for i in range(w):
        for j in range(h):
            img[i][j] = p[img[i][j]]
plt.plot(cal_h(img))
plt.show()
# vd 
# 6  4  1  2
# 3  5  7  2
# 1  4  4  1
# 3  8  1  7
# 2  2  4  3
# -----------------------
# bước 1 : 
# ri  (giá trị điểm ảnh)  1  2  3  4  5  6  7  8
# pri( sô lần xuất hiện)  4  4  3  4  1  1  2  1

# bước 2: L = 8 (max(img)) , w * h = 4 * 5 ( 4 cột 5 hàng)
# ri  (giá trị điểm ảnh)  1     2    3    4     5     6    7  8
# pri( sô lần xuất hiện)  4     4    3    4     1     1   2    1
# new pri                 1.6  1.6  1.2  1.6   0.4  0.4  0.8  0.4
# Bước 3 : cộng dồn       1.6  3.2  4.4  6     6.4  6.8  7.6  8.0
# bước 4 : làm tròn       2    3    4    6     6    7    8    8
# bước 5 : anh xa         img[i][j] = p[img[i][j]]