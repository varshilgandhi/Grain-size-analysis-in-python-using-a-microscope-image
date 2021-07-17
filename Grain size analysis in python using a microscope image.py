# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 19:37:12 2021

@author: abc
"""


"""

Step : 1 Read image and define size (if needed to convert results into microns , not pixels)
step : 2 Denoising if required and threshold image to separate grains from grains
step : 3 Clean up image , if needed (erode,etc.) and create a mask for grains
step : 4 Label grains in the masked image
step : 5 Measure the properties of each grain (object)
step : 6 Output results into a csv file


"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import io, color, measure

#step : 1  Read image and define size (if needed to convert results into microns , not pixels)

img = cv2.imread("grains2.jpg",cv2.IMREAD_GRAYSCALE);
pixels_to_um = 0.5   # 1 pixel = 0.5 um or 500nm

#step : 2  Denoising if required and threshold image to separate grains from grains
#denoising not required
#plt.hist(img.flat, bins = 100, range=(0,255))

ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#step : 3  Clean up image , if needed (erode,etc.) and create a mask for grains

kernel = np.ones((3,3),np.uint8)
eroded= cv2.erode(thresh, kernel, iterations = 1)
dilated= cv2.dilate(eroded, kernel, iterations = 1)

#create a mask for grains
mask = dilated == 255

#step : 4  Label grains in the masked image

s = [[1,1,1],[1,1,1],[1,1,1]]
labeled_mask, num_labels = ndimage.label(mask, structure=s)

img2 = color.label2rgb(labeled_mask, bg_label=0)

cv2.imshow('Colored Grains',img2)
cv2.waitKey(0)


#step : 5 Measure the properties of each grain (object)


clusters = measure.regionprops(labeled_mask, img)

#step : 6 Output results into a csv file


propList = ['Area',
            'equivalent_diameter',
            'orientation',
            'MajorAxisLength',
            'MinorAxisLength',
            'perimeter',
            'MinIntensity',
            'MeanIntensity',
            'MaxIntensity']

output_file = open('image_measurements.csv', 'w')
output_file.write(',' + ",".join(propList) + '\n')

for cluster_props in clusters:
    #output cluster properties to the excel file
    output_file.write(str(cluster_props['Label']))
    for i, prop in enumerate(propList):
        if(prop == 'Area'):
            to_print = cluster_props[prop]*pixels_to_um**2  #Convert pixel square to micro
        elif(prop == 'orientation'):
            to_print = cluster_props[prop]*57.2958   #Convert to degrees from radians
        elif(prop.find('Intencity') <0):               #Any prop without intensity 
            to_print = cluster_props[prop]*pixels_to_um
        else:
            to_print = cluster_props[prop]             #Remaining props 
        output_file.write(',' + str(to_print))
    output_file.write('\n')






cv2.imshow("Thresholded Image",thresh)
cv2.imshow("eroded Image",eroded)
cv2.imshow("dialated Image",dilated)
cv2.waitKey(0)








