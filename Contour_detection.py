# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 16:46:23 2017

@author: ks
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
import glob
cv_img = []
path = "./Sim_with_table/Cloth6"
x_val = np.arange(255)
for img in sorted(glob.glob(path+"/00*.jpg")):
	n = cv2.imread(img)
	cv_img.append(n)

# Gabor filters
def build_filters():
	filters = []
	ksize = 31
	for theta in np.arange(0, np.pi, np.pi/16):
		kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
		kern /= 1.5 * kern.sum()
		filters.append(kern)
	return filters

 
def process(img, filters):
	accum = np.zeros_like(img)
	for kern in filters:
		fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
		np.maximum(accum, fimg, accum)	
	return accum


# blur size = (9,9)
# imgweight = 1.5
# gaussianweight = -0.5
# 2.5 -1.5
def unsharp_mask(img, blur_size = (15,15), imgWeight = 2.5, gaussianWeight = -1.5):
    gaussian = cv2.GaussianBlur(img, (5,5), 0)
    return cv2.addWeighted(img, imgWeight, gaussian, gaussianWeight, 0)
j =1
max_area=[]
max_perimeter = []
for img in cv_img:
	# Finding the edges of tablecloth
	img = cv2.blur(img, (5, 5))
	img = unsharp_mask(img)
	img = unsharp_mask(img)
	img = unsharp_mask(img)

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)

	thresh = cv2.adaptiveThreshold(s, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
	_, contours, heirarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(contours, key = cv2.contourArea, reverse = True)
	#for cnt in cnts:
	canvas_for_contours = thresh.copy()
	cv2.drawContours(thresh, cnts[:-1], 0, (0,255,0), 3)
	cv2.drawContours(canvas_for_contours, contours, 0, (0,255,0), 3)
	ed = canvas_for_contours - thresh
	
	#Making contour
	A=[] #area list
	P=[] #perimeter list
	image, contours, hierarchy = cv2.findContours(ed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	filters = build_filters()
	 
	res1 = process(ed, filters)
	

	for cnt in contours:
		hull = cv2.convexHull(cnt)
		cv2.drawContours(img, [hull], -1, (0,0,255),3 )

		perimeter = cv2.arcLength(cnt,True)
		area = cv2.contourArea(cnt)
		A.append(area)
		P.append(perimeter)

		#print("Area : ", max(A))
		#print("Perimeter : ", max(P))
		max_area.append(max(A))
		max_perimeter.append(max(P))
	cv2.imshow('Result', img )
	sav_file = path+ "/contour/Contour_%d.jpg"%j
	#print(sav_file)
	cv2.imwrite(sav_file, img)
	j = j+1
	#print("image saved")
	cv2.waitKey(50)
print(len(max_area))
print(len(max_perimeter))

frames = np.linspace(1,len(max_area), len(max_area))
fig, ax = plt.subplots(nrows=1, ncols=2)
plt.subplot(1,2,1)
if max_area!=0:
	plt.plot(frames, max_area, 'r', label="area of contour")
plt.title("Area")
plt.legend()
plt.xlabel("frames")
plt.ylabel("area")
plt.subplot(1,2,2)
if max_perimeter!=0:
	plt.plot(frames, max_perimeter, 'b', label="perimeter of contour")
plt.legend()
plt.xlabel("frames")
plt.ylabel("perimeter")
plt.title("Perimeter")
plt.show()
