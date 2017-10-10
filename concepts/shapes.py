class Shape:

	def __init__(self, contour, index=-1, rank=-1, parent=None, children=[], program=None):
		self.contour = contour
		self.index = index
		self.rank = rank
		self.parent = parent
		self.children = children
		self.program = program
		self.type = ""

	def addChild(self, child):
		self.children.append(child)

	def flatParams(self):
		return self.program.flatParams()

# class ShapeTree:

# 	def __init__(self, contours, hierarchy):

def buildShapeTree(contours, hierarchy):
	shapes = []
	for i in range(len(contours)):
		contour = contours[i]
		if hierarchy[i][3] == -1:
			shapes.append(Shape(contour, i, 0, None, []))
		else:
			parent = shapes[hierarchy[i][3]]
			rank = shapes[parent.index].rank + 1
			shapes.append(Shape(contour, i, rank, parent, []))
			shapes[parent.index].addChild(shapes[i])
	return shapes

	# def __init__(self, contours, hierarchy):
	# 	self.shapes = [Shape(contours[0], 0, 0, None, [])]
	# 	for i in range(1, len(contours)):
	# 		contour = contours[i]
	# 		parent = self.shapes[hierarchy[i][3]]
	# 		rank = self.shapes[parent.index].rank + 1
	# 		self.shapes.append(Shape(contour, i, rank, parent, []))
	# 		self.shapes[parent.index].addChild(self.shapes[i])