import cv2
import cairo.tree as ct
import imutils
import math

scale_size = 256

class Shape:

	def __init__(self, contour, index=-1, rank=-1, parent=None, children=[], program=None):
		self.contour = contour
		self.index = index
		self.rank = rank
		self.parent = parent
		self.children = children
		self.program = program

	def addChild(self, child):
		self.children.append(child)

class ShapeTree:

	def __init__(self, contours, hierarchy):
		self.shapes = [Shape(contours[0], 0, 0, None, [])]
		for i in range(1, len(contours)):
			contour = contours[i]
			parent = self.shapes[hierarchy[i][3]]
			rank = self.shapes[parent.index].rank + 1
			self.shapes.append(Shape(contour, i, rank, parent, []))
			self.shapes[parent.index].addChild(self.shapes[i])

def encode(image, preview=False):
	resized = imutils.resize(image, width=scale_size)
	ratio = image.shape[0]/float(scale_size)
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	image2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
		cv2.CHAIN_APPROX_SIMPLE)
	hierarchy = hierarchy[0]
	prog = ct.Pr([])
	shapes = ShapeTree(contours, hierarchy)

	for i in range(1, len(contours)):
		c = contours[i]
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04*peri, True)
		M = cv2.moments(c)
		cX = (M["m10"] / M["m00"]) / float(scale_size)
		cY = (M["m01"] / M["m00"]) / float(scale_size)
		center = ct.Po((cX, cY))

		if len(approx) == 4:
			component = ct.Sq(center, math.sqrt(cv2.contourArea(c))/float(scale_size))
			prog.addComponent(component)
			shapes.shapes[i].program = component

		if len(approx) > 5:
			component = ct.Ci(center, (math.sqrt(cv2.contourArea(c)/math.pi))/float(scale_size))
			prog.addComponent(component)
			shapes.shapes[i].program = component

	shapes.shapes[0].program = prog

	if preview: prog.preview()
	return shapes