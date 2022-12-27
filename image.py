import cv2 
import numpy as np
from PIL import Image,ImageFilter
from rembg import remove 
img = cv2.imread('3.jpg')  
img = cv2.resize(img, dsize=(1000, 800))
cv2.imwrite('3.jpg',img)

#tking input
r = cv2.selectROI('area',img)

#cropping image

cropped_image = img[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])]
cv2.imwrite('small.jpg',cropped_image)
input_path = 'small.jpg'
output_path = 'output.png'

#Removing Background

input = Image.open(input_path)
output = remove(input)
output.save(output_path)

#Finding edges of image

image = Image.open('output.png')
image = image.filter(ImageFilter.CONTOUR)
image.save('edges.png') 


#Changing color of edges

m =  cv2.imread("edges.png")

h,w,bpp = np.shape(m)

color=(0,255,0)
for py in range(h-1,1,-1):
    for px in range(w-1,1,-1):
        if(m[py][px][0]!=255 and m[py][px][1]!=255 and px+1<w-1 and py+1<h-1):           
           cv2.line(m, (px-2,py),(px+2,py), color, thickness=1)
           #cv2.line(m, (px,py+5),(px,py-5), color, thickness=1)

#and px+1<w-1 and py+1<h-1

cv2.imwrite('yourNewImage.jpg',m)

#overlaying image with edges to cropped image

from PIL import Image
img2 = Image.open('yourNewImage.jpg')
mask_card = Image.open("output.png").convert("RGBA")
img2.paste(mask_card,(0,0),mask_card)
   

# overlaying bordered image to original image

img2 = remove(img2)
img2.save('new2.png')
img3= Image.open('3.jpg')
mask_card = Image.open('new2.png').convert("RGBA")
img3.paste(mask_card,(int(r[0]),int(r[1])),mask_card)
img3.save('final.png')

#display image
final=cv2.imread('final.png')
cv2.imshow('boundary',final)
cv2.waitKey()
