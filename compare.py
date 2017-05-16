from PIL import Image
import numpy as np
import logging
import datetime, time
import re
import warnings
import cv2
from matplotlib import pyplot as plt
import rendermp
import math

np.set_printoptions(threshold=np.inf) # this is to print full numpy arrays
warnings.filterwarnings("ignore") # a little dangerous... but I'm doing this for now to suppress
# all the annoying RuntimeWarning: overflow encountered in ubyte_scalars that show when dist gets big

def edge_hausdorff(img1, img2):
	if not img1.shape == img2.shape:
		logging.warning("edge_hausdorff: attempted to compare two images that are not the same shape")
	edge1 = cv2.Canny(img1,100,200) # thresholds may need tweaking?
	edge2 = cv2.Canny(img2,100,200)
	return max_hausdorff(edge1, edge2)

def avg_hausdorff(edge1, edge2):
	A = []
	B = []
	for i in range(0,edge1.shape[0]):
		for j in range(0,edge1.shape[1]):
			if edge1[i][j] == 255:
				A.append([i,j])
			if edge2[i][j] == 255:
				B.append([i,j])

	hBA = 0
	for i in range(len(A)):
		mindist = np.inf
		for j in range(len(B)):
			dist = math.sqrt(((A[i][0]-B[j][0])**2+(A[i][1]-B[j][1])**2))
			mindist = min(mindist, dist)
		hBA += mindist
	hBA = hBA/len(A)

	hAB = 0
	for i in range(len(B)):
		mindist = np.inf
		for j in range(len(A)):
			dist = math.sqrt(((B[i][0]-A[j][0])**2+(B[i][1]-A[j][1])**2))
			mindist = min(mindist, dist)
		hAB += mindist
	hAB = hAB/len(B)
	
	return max(hAB,hBA)

def max_hausdorff(edge1, edge2):
	A = []
	B = []
	for i in range(0,edge1.shape[0]):
		for j in range(0,edge1.shape[1]):
			if edge1[i][j] == 255:
				A.append([i,j])
			if edge2[i][j] == 255:
				B.append([i,j])

	hBA = 0
	for i in range(len(A)):
		mindist = np.inf
		for j in range(len(B)):
			dist = math.sqrt(((A[i][0]-B[j][0])**2+(A[i][1]-B[j][1])**2))
			mindist = min(mindist, dist)
		hBA = max(hBA, mindist)

	hAB = 0
	for i in range(len(B)):
		mindist = np.inf
		for j in range(len(A)):
			dist = math.sqrt(((B[i][0]-A[j][0])**2+(B[i][1]-A[j][1])**2))
			mindist = min(mindist, dist)
		hAB = max(hAB, mindist)
	
	return max(hAB,hBA)

def compareleastsquares(img1, img2): # img1, img2 are ndarrays; least squares
	if not img1.shape == img2.shape:
		logging.warning("compareleastsquares: attempted to compare two images that are not the same shape.")
	flat1 = img1.flatten()
	flat2 = img2.flatten()
	dist = 0
	for i in range(flat1.size):
		dist += (flat1[i] - flat2[i])**2
	return dist

def compareabs(img1, img2): # img1, img2 are ndarrays; sum of absolute value of distance between pixels
	if not img1.shape == img2.shape:
		logging.warning("compareleastsquares: attempted to compare two images that are not the same shape.")
	flat1 = img1.flatten()
	flat2 = img2.flatten()
	dist = 0
	for i in range(flat1.size):
		dist += abs(flat1[i] - flat2[i])
	return dist

# if __name__ == "__main__":
# 	name = "mplog"+re.sub(r' ', '-', re.sub(r':', '-', str(datetime.datetime.now())))
# 	logging.basicConfig(filename="./log/"+name, level=logging.DEBUG)
# 	srcimg = Image.open("./images/SampleImage.png").convert('L')
# 	testimg = rendermp.renderImage('''fill fullcircle scaled 15 shifted (32,17) withcolor black;''')
# 	print edge_hausdorff(np.array(srcimg), np.array(testimg))