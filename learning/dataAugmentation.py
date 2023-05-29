import os
from glob import glob
import cv2
from IPython.display import Image, display
import numpy as np

Path = glob("./meta/*")

#明るさコントラスト調整
def adjust(img, contrast=1.0, brightness=0.0):
  # 積和演算を行う。
  dst = contrast * img + brightness
  # [0, 255] でクリップし、uint8 型にする。
  return np.clip(dst, 0, 255).astype(np.uint8)


for file in Path:
  files = os.listdir(file)
  print(file)
  for image in files:
    image.endswith(".jpg")
    img = cv2.imread(file+"/"+image)
    title, ext = os.path.splitext(image)
    image0 = adjust(img, contrast=0.2, brightness=1.0)
    cv2.imwrite(file + "/" + title + "_0.2" + ext, image0)
    image1 = adjust(img, contrast=0.4, brightness=1.0)
    cv2.imwrite(file + "/" + title + "_0.4" + ext, image1)
    image2 = adjust(img, contrast=0.6, brightness=1.0)
    cv2.imwrite(file + "/" + title + "_0.6" + ext, image2)
    image3 = adjust(img, contrast=0.8, brightness=1.0)
    cv2.imwrite(file + "/" + title + "_0.8" + ext, image3)
    image4 = adjust(img, contrast=1.3, brightness=1.0)
    cv2.imwrite(file + "/" + title + "_1.3" + ext, image4)
    image5 = adjust(img, contrast=1.6, brightness=1.0)
    cv2.imwrite(file + "/" + title + "_1.6" + ext, image5)


#明るさ半分
for file in Path:
  files = os.listdir(file)
  for image in files:
    image.endswith(".jpg")
    img = cv2.imread(file+"/"+image)
    half_img = img // 2
    title, ext = os.path.splitext(image)  
    cv2.imwrite(file + "/" + title + "_half" + ext, half_img)


#45度ずつ回転
for file in Path:
  files = os.listdir(file)
  for image in files:
    image.endswith(".jpg")
    img = cv2.imread(file+"/"+image)
    h,w,s = img.shape
    M = cv2.getRotationMatrix2D((w/2, h/2), 45, 1)
    image0 = cv2.warpAffine(img, M, (480, 640))
    M = cv2.getRotationMatrix2D((w/2, h/2), 135, 1)
    image1 = cv2.warpAffine(img, M, (480, 640))
    M = cv2.getRotationMatrix2D((w/2, h/2), 225, 1)
    image2 = cv2.warpAffine(img, M, (480, 640))
    M = cv2.getRotationMatrix2D((w/2, h/2), 315, 1)
    image3 = cv2.warpAffine(img, M, (480, 640))
    title, ext = os.path.splitext(image)

    cv2.imwrite(file + "/" + title + "_45" + ext, image0)
    cv2.imwrite(file + "/" + title + "_135" + ext, image1)
    cv2.imwrite(file + "/" + title + "_225" + ext, image2)
    cv2.imwrite(file + "/" + title + "_315" + ext, image3)


# #上下左右反転
for file in Path:
  files = os.listdir(file)
  for image in files:
    image.endswith(".jpg")
    img = cv2.imread(file+"/"+image)
    img = cv2.resize(img, (480, 640))
    image0 = cv2.flip(img,0)
    image1 = cv2.flip(img,1)
    image2 = cv2.flip(img,-1)
    title, ext = os.path.splitext(image)

    cv2.imwrite(file + "/" + title + "_up" + ext, image0)
    cv2.imwrite(file + "/" + title + "_left" + ext, image1)
    cv2.imwrite(file + "/" + title + "_upandleft" + ext, image2)
