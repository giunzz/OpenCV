import cv2
import numpy as np

def cov(img,k):
    #maxg = np.max(img)
    #I = [0] * (maxg + 1)
    I=np.zeros(img.shape)
    iw,ih=img.shape
    kw,kh=k.shape
    print(iw, ih, kw, kh)
    for i in range(iw):
        for j in range(ih):
            s=0
            for u in range(kw):
                for v in range(kh):
                    uu=i+u-kw//2
                    vv=j+v-kh//2
                    if uu<0 or vv<0 or uu>=iw or vv>=ih: continue
                    s+=(k[u][v]*img[uu][vv])
            I[i][j]=s
    return I
sobel1=np.array([[-1,0,1],
                [-2,0,2],
                [-1,0,1]])
sobel2=np.array([[-1,-2,-1],
                [0,0,0],
                [1,2,1]])
img = cv2.imread("b.jpg",0)

simg1=cv2.convertScaleAbs(cov(img,sobel1))
simg2=cv2.convertScaleAbs(cov(img,sobel2))
sobel=simg1+simg2
cv2.imshow('Img',img)
cv2.imshow('Sobel1',simg1)
cv2.imshow('Sobel2',simg2)
cv2.imshow('Sobel',sobel)

ret, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
img_copy = img.copy()
cv2.drawContours(image=img_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
cv2.imshow('None approximation', img_copy)

print(len(contours))
hull = []
for i in range(len(contours)):
    hull.append(cv2.convexHull(contours[i], False))
i=0
for h in contours:
    print(i)
    x,y,w,h=cv2.boundingRect(h)
    tmpi=img[y-2:y+h+2,x-1:x+w+1]
    cv2.imwrite("img/"+str(i)+".jpg",tmpi)
    i+=1

cv2.waitKey(0)
cv2.destroyAllWindows()