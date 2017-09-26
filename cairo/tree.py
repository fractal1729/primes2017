import config
import cairocffi as cairo
import numpy as np
import io
import math
import random
from PIL import Image
import copy
import utils
import cv2

# Constants

WIDTH = config.CANVAS_SIZE
HEIGHT = config.CANVAS_SIZE
RED = (255, 0, 0)
GREEN = (0, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# SEE BOTTOM FOR SHORTCUTS

# Definitions

class Program:

	def __init__(self, components=None):
		if components != None: self.components = components
		else: self.components = [Square()]

	def addComponent(self, component):
		self.components.append(component)

	def draw(self):
		surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
		cr = cairo.Context(surface)

		cr.set_source_rgb(255, 255, 255)
		cr.paint()
		cr.set_source_rgb(0, 0, 0)

		cr.scale(WIDTH, HEIGHT)
		cr.set_line_width(0.01)

		for component in self.components:
			component.draw(cr)

		data = surface.write_to_png(None)
		image = Image.open(io.BytesIO(data))
		return utils.RGB2BGR(np.asarray(image))

	def preview(self):
		pix = self.draw()
		cv2.imshow("Program Preview", pix)
		cv2.waitKey(0)

class PointSet: # in the future, I might want to make a more general version of this class
# that allows me to make patterns out of non point objects.

	def __init__(self, points=None):
		if points != None: self.points = points
		else: self.points = []

	def addPoint(self, point):
		self.points.append(point)

	def preview(self):
		pr = Pr([])
		for p in self.points:
			pr.addComponent(Ci(p, 0.01, (0, 0, 255), True))
		pr.preview()

	def size(self):
		return len(self.points)

	def getPoint(self, index):
		return self.points[index]

# Compositional objects

class Tufa:

	def __init__(self, center=None, sidelength=None, r1=None, r2=None, color=(0, 255, 0),
		color1=(255, 0, 0), color2=(255, 0, 0)):
		self.center = Point(center)
		self.sidelength = Numeric()

class Hugh:

	def __init__(self, center=None, sidelength=None, color=(0, 0, 0), color1=(0, 255, 0)):
		self.center = center
		self.radius = Numeric(radius, 0.02, min(min(self.center.x.val, 1-self.center.x.val), min(self.center.y.val, 1-self.center.y.val)))
		self.color = [color[0]/255.0, color[1]/255.0, color[2]/255.0]
		self.color1 = [color1[0]/255.0, color1[1]/255.0, color1[2]/255.0]
		self.square = Square(self.center, self.sidelength, self.color)
		self.circle = Circle(self.center, self.sidelength.val/4, self.color1)

	def draw(self, cr):
		self.square.draw()
		self.circle.draw()

# Primitives

class Circle:
	
	def __init__(self, center=None, radius=None, color=(0, 0, 0), boundOverride=False, fill=True):
		self.center = Point(center)
		if boundOverride: self.radius = Numeric(radius)
		else: self.radius = Numeric(radius, 0.005, min(min(self.center.x.val, 1-self.center.x.val), min(self.center.y.val, 1-self.center.y.val)))
		self.fill = fill
		self.color = [color[0]/255.0, color[1]/255.0, color[2]/255.0]

	def draw(self, cr):
		cr.set_source_rgb(self.color[0], self.color[1], self.color[2])
		cr.arc(self.center.x.val, self.center.y.val, self.radius.val, 0, 2*math.pi)
		if self.fill: cr.fill()
		else: cr.stroke()

	def __repr__(self):
		return ("Circle(center=("+str(self.center.x.val)+", "+str(self.center.y.val)+"), radius="
			+str(self.radius.val)+", color=("+str(self.color[0])+", "+str(self.color[1])+", "+str(self.color[2])+"))")

class Square:
	
	def __init__(self, center=None, sidelength=None, color=(0, 0, 0), fill=True):
		self.center = Point(center)
		self.sidelength = Numeric(sidelength, 0.015, 2*min(min(self.center.x.val, 1-self.center.x.val), min(self.center.y.val, 1-self.center.y.val)))
		self.fill = fill
		self.color = [color[0]/255.0, color[1]/255.0, color[2]/255.0]

	def draw(self, cr):
		cr.set_source_rgb(self.color[0], self.color[1], self.color[2])
		cr.rectangle(self.center.x.val - self.sidelength.val/2, self.center.y.val - self.sidelength.val/2,
			self.sidelength.val, self.sidelength.val)
		if self.fill: cr.fill()
		else: cr.stroke()

	def __repr__(self):
		return ("Square(center=("+str(self.center.x.val)+", "+str(self.center.y.val)+"), sidelength="
			+str(self.sidelength.val)+", color=("+str(self.color[0])+", "+str(self.color[1])+", "+str(self.color[2])+"))")

class Rectangle:

	def __init__(self, center=None, width=None, height=None, color=(0, 0, 0), fill=True):
		self.center = Point(center)
		self.width = Numeric(width, 0.03, 2*min(self.center.x.val, 1-self.center.x.val))
		self.height = Numeric(height, 0.03, 2*min(self.center.y.val, 1-self.center.y.val))
		self.fill = fill
		self.color = [color[0]/255.0, color[1]/255.0, color[2]/255.0]

	def draw(self, cr):
		cr.set_source_rgb(self.color[0], self.color[1], self.color[2])
		cr.rectangle(self.center.x.val - self.width.val/2, self.center.y.val - self.height.val/2, self.width.val, self.height.val)
		if self.fill: cr.fill()
		else: cr.stroke()

	def __repr__(self):
		return ("Rectangle(center="+str(self.center.x.val)+", "+str(self.center.y.val)+"), width="
			+str(self.width.val)+", height="+str(self.height.val)+", color=("+str(self.color[0])
			+", "+str(self.color[1])+", "+str(self.color[2])+"))")

class Point:

	def __init__(self, coords=None):
		if not coords: coords = (None, None)
		if isinstance(coords, Point):
			self.x = coords.x
			self.y = coords.y
		if not isinstance(coords, Point):
			self.x = Numeric(coords[0])
			self.y = Numeric(coords[1])
		
	def __str__(self):
		return "("+str(self.x)+", "+str(self.y)+")"

	def __repr__(self):
		return "Point("+str(self.x)+", "+str(self.y)+")"

# class NumericRange:

# 	def __init__(self, minVal=0, maxVal=1):
# 		self.minVal = minVal
# 		self.maxVal = maxVal

# 	def compare(self, )

class Numeric: # coordinate or length, float between 0 and 1

	def __init__(self, val=None, minVal=None, maxVal=None):
		if isinstance(val, Numeric):
			self.minVal = minVal if minVal else val.minVal
			self.maxVal = maxVal if maxVal else val.maxVal
			if val.val >= self.minVal and val.val <= self.maxVal: self.val = val.val
			else: print "Error: tried to initialize Numeric out of range."
		else:
			self.minVal = minVal if minVal else 0
			self.maxVal = maxVal if maxVal else 1
			if val:
				if val >= self.minVal and val <= self.maxVal: self.val = val
				else: print "Error: tried to initialize Numeric out of range."
			else: self.val = random.random()*(self.maxVal-self.minVal) + self.minVal

	def __add__(self, other):
		if isinstance(other, Numeric):
			return Numeric(self.val + other.val)
		return self.val + val

	def __iadd__(self, val):
		self.val += val
		return self

	def __str__(self):
		return str(self.val)

	def __repr__(self):
		return 'Numeric(%s)' % self.val



# Shortcuts

Pr = Program
Ci = Circle
Sq = Square
Re = Rectangle
Po = Point
Nu = Numeric