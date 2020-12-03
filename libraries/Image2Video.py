import cv2
import numpy as np
import os
from datetime import datetime,date,timedelta
import sys

fps = 8
img_array = []
names = os.listdir('./frame')
times =sorted([datetime.strptime(dt.split('.')[0], "%d-%m-%Y-%H-%M-%S-%f") for dt in names])
ImageNames = []
for d in times:
    ImageNames.append(d.strftime("%d-%m-%Y-%H-%M-%S-%f")+'.jpg')
#print(ImageNames)

for filename in ImageNames:
    print(filename)
    img = cv2.imread('./frame//'+filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('sample.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()