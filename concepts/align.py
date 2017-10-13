import numpy as np
import math

def findCenterAlignments(shapes):
	return findAlignments([(shape.program.center.x.val, shape.program.center.y.val) for shape in shapes])

# straightforward O(N^3) implementation
# for every line between two points I run through all the other points and see who else is on that line
def findAlignments(points):
	lines = [] # uses indices of points as opposed to the points themselves!
	for i in range(len(points)):
		for j in range(i+1, len(points)):
			x1 = points[i][0]
			y1 = points[i][1]
			x2 = points[j][0]
			y2 = points[j][1]
			# ax + by + c = 0
			a = y1-y2
			b = x2-x1
			c = y2*x1 - x2*y1
			collinearpts = set([i,j])
			for k in range(len(points)):
				if k != i and k != j:
					dist = abs(a*points[k][0]+b*points[k][1]+c)/math.sqrt(a*a+b*b)
					if dist < 0.005:
						collinearpts.add(k)
			if len(collinearpts) > 2:
				lines.append(frozenset(collinearpts))
	return list(set(lines))

	

# O(N^2) attempt:
# def findAlignments(points):
	# lines = [] # pairs of the form (m, b) for lines y = mx+b
	# for i in range(len(points)):
	# 	for j in range(i+1, len(points)):
	# 		x1 = points[i][0]
	# 		y1 = points[i][1]
	# 		x2 = points[j][0]
	# 		y2 = points[j][1]
	# 		m = (y2-y1)/(x2-x1)
	# 		b = (y1x2-y2x1)/(x2-x1)
	# 		addLine(lines, (m, b))
#
# def addLine(lines, newline):
# 	m, b = newline
# 	for (M, B) in lines:
# 		if -0.05 < np.arctan(M) - np.arctan(m) and np.arctan(M) - np.arctan(m) < 0.05:
# 			if -0.04 < B - b < 0.04:
# 				return
# 	lines.append(newline)
# 	# this is pretty sketch...