import cv2
import cairo.tree as ct
import imutils
import math
import numpy as np
from concepts.shapes import Shape, buildShapeTree

scale_size = 256

def stripInners(contours, hierarchy):
	# the contours detected after Canny edge detection include both the outer and inner
	# contours for each closed shape, so this function strips all the inner ones.
	# hierarchy: [Next, Previous, First child, Parent]
	newcontours = []
	newhierarchy = []
	for i in range(len(contours)/2):
		newcontours.append(contours[2*i])
		nexti = hierarchy[2*i][0]/2
		previousi = hierarchy[2*i][1]/2
		childi = hierarchy[2*i+1][2]/2 # -1/2 = -1
		parenti = (hierarchy[2*i][3]-1)/2 # -1/2 = -1
		newhierarchy.append([nexti, previousi, childi, parenti])
	return newcontours, newhierarchy

def findEdges(image, lower, upper):
	blue = image[:, :, 0]
	green = image[:, :, 1]
	red = image[:, :, 2]
	bedge = cv2.Canny(blue, lower, upper)
	gedge = cv2.Canny(green, lower, upper)
	redge = cv2.Canny(red, lower, upper)
	union = np.zeros(image.shape[:2], dtype='uint8')
	for i in range(union.shape[0]):
		for j in range(union.shape[1]):
			if bedge[i][j] > 0 or gedge[i][j] > 0 or redge[i][j] > 0: union[i][j] = 255
	return union

def encode(image, preview=False):
	resized = imutils.resize(image, width=scale_size)
	ratio = image.shape[0]/float(scale_size)
	# gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	# edged = cv2.Canny(gray, 2, 200)
	edged = findEdges(resized, 30, 200)
	# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	# thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	image2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE,
		cv2.CHAIN_APPROX_SIMPLE)
	hierarchy = hierarchy[0]
	contours, hierarchy = stripInners(contours, hierarchy)
	prog = ct.Pr([])
	shapes = buildShapeTree(contours, hierarchy)

	for i in range(len(contours)):
		c = contours[i]
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04*peri, True)
		M = cv2.moments(c)
		cX = (M["m10"] / M["m00"]) / float(scale_size)
		cY = (M["m01"] / M["m00"]) / float(scale_size)
		center = ct.Po((cX, cY))

		maskcontours = [c]
		child_index = hierarchy[i][2]
		while child_index != -1:
			maskcontours.append(contours[child_index])
			child_index = hierarchy[child_index][0]
		mask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.drawContours(mask, maskcontours, -1, 255, -1)
		mask = cv2.erode(mask, None, iterations=2)
		colorBGR = cv2.mean(image, mask=mask)[:3]
		colorRGB = [colorBGR[2], colorBGR[1], colorBGR[0]] # BGR -> RGB

		if len(approx) == 4:
			(x, y, w, h) = cv2.boundingRect(approx)
			component = None
			if float(w)/float(h) >= 0.95 and float(w)/float(h) <= 1.05:
				component = ct.Sq(center, math.sqrt(w*h)/float(scale_size), colorRGB)
				shapes[i].type = "sq"
			else:
				component = ct.Re(center, w/float(scale_size), h/float(scale_size), colorRGB)
				shapes[i].type = "re"
			prog.addComponent(component)
			shapes[i].program = component

		if len(approx) > 5:
			component = ct.Ci(center, (math.sqrt(cv2.contourArea(c)/math.pi))/float(scale_size), colorRGB)
			prog.addComponent(component)
			shapes[i].program = component
			shapes[i].type = "ci"

	if preview: prog.preview()
	return prog, shapes

# gray5 = cv2.cvtColor(pix5, cv2.COLOR_BGR2GRAY)
# blurred5 = cv2.GaussianBlur(gray5, (5, 5), 0)
# thresh5 = cv2.threshold(blurred5, 60, 255, cv2.THRESH_BINARY)[1]
# image5, contours5, hierarchy5 = cv2.findContours(thresh5.copy(), cv2.RETR_TREE,	cv2.CHAIN_APPROX_SIMPLE)