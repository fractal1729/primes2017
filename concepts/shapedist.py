import utils, math
import numpy as np

def distanceMatrix(shapes):
	D = np.zeros((len(shapes),len(shapes)))
	for i in range(len(shapes)):
		for j in range(len(shapes)):
			if i != j:
				p1 = shapes[i].program
				p2 = shapes[j].program
				if shapes[i].type == "ci":
					if shapes[j].type == "ci":
						D[i][j] = circle2circleDist(p1.center.x.val, p1.center.y.val, p1.radius.val,
							p2.center.x.val, p2.center.y.val, p2.radius.val,
							utils.isInside(shapes[i], shapes[j]), utils.isInside(shapes[j], shapes[i]))
					if shapes[j].type == "re":
						D[i][j] = circle2rectDist(p1.center.x.val, p1.center.y.val, p1.radius.val,
							p2.center.x.val-p2.width.val/2, p2.center.x.val+p2.width.val/2,
							p2.center.y.val-p2.height.val/2, p2.center.y.val+p2.height.val/2,
							utils.isInside(shapes[i], shapes[j]), utils.isInside(shapes[j], shapes[i]))
					if shapes[j].type == "sq":
						D[i][j] = circle2rectDist(p1.center.x.val, p1.center.y.val, p1.radius.val,
							p2.center.x.val-p2.sidelength.val/2, p2.center.x.val+p2.sidelength.val/2,
							p2.center.y.val-p2.sidelength.val/2, p2.center.y.val+p2.sidelength.val/2,
							utils.isInside(shapes[i], shapes[j]), utils.isInside(shapes[j], shapes[i]))
				if shapes[i].type == "re":
					if shapes[j].type == "ci":
						D[i][j] = circle2rectDist(p2.center.x.val, p2.center.y.val, p2.radius.val,
							p1.center.x.val-p1.width.val/2, p1.center.x.val+p1.width.val/2,
							p1.center.y.val-p1.height.val/2, p1.center.y.val+p1.height.val/2,
							utils.isInside(shapes[j], shapes[i]), utils.isInside(shapes[i], shapes[j]))
					if shapes[j].type == "re":
						D[i][j] = rect2rectDist(p1.center.x.val-p1.width.val/2, p1.center.x.val+p1.width.val/2,
							p1.center.y.val-p1.height.val/2, p1.center.y.val+p1.height.val/2,
							p2.center.x.val-p2.width.val/2, p2.center.x.val+p2.width.val/2,
							p2.center.y.val-p2.height.val/2, p2.center.y.val+p2.height.val/2,
							utils.isInside(shapes[i], shapes[j]), utils.isInside(shapes[j], shapes[i]))
					if shapes[j].type == "sq":
						D[i][j] = rect2rectDist(p1.center.x.val-p1.width.val/2, p1.center.x.val+p1.width.val/2,
							p1.center.y.val-p1.height.val/2, p1.center.y.val+p1.height.val/2,
							p2.center.x.val-p2.sidelength.val/2, p2.center.x.val+p2.sidelength.val/2,
							p2.center.y.val-p2.sidelength.val/2, p2.center.y.val+p2.sidelength.val/2,
							utils.isInside(shapes[i], shapes[j]), utils.isInside(shapes[j], shapes[i]))
				if shapes[i].type == "sq":
					if shapes[j].type == "ci":
						D[i][j] = circle2rectDist(p2.center.x.val, p2.center.y.val, p2.radius.val,
							p1.center.x.val-p1.sidelength.val/2, p1.center.x.val+p1.sidelength.val/2,
							p1.center.y.val-p1.sidelength.val/2, p1.center.y.val+p1.sidelength.val/2,
							utils.isInside(shapes[j], shapes[i]), utils.isInside(shapes[i], shapes[j]))
					if shapes[j].type == "re":
						D[i][j] = rect2rectDist(p1.center.x.val-p1.sidelength.val/2, p1.center.x.val+p1.sidelength.val/2,
							p1.center.y.val-p1.sidelength.val/2, p1.center.y.val+p1.sidelength.val/2,
							p2.center.x.val-p2.width.val/2, p2.center.x.val+p2.width.val/2,
							p2.center.y.val-p2.height.val/2, p2.center.y.val+p2.height.val/2,
							utils.isInside(shapes[i], shapes[j]), utils.isInside(shapes[j], shapes[i]))
					if shapes[j].type == "sq":
						D[i][j] = rect2rectDist(p1.center.x.val-p1.sidelength.val/2, p1.center.x.val+p1.sidelength.val/2,
							p1.center.y.val-p1.sidelength.val/2, p1.center.y.val+p1.sidelength.val/2,
							p2.center.x.val-p2.sidelength.val/2, p2.center.x.val+p2.sidelength.val/2,
							p2.center.y.val-p2.sidelength.val/2, p2.center.y.val+p2.sidelength.val/2,
							utils.isInside(shapes[i], shapes[j]), utils.isInside(shapes[j], shapes[i]))
				#print D[i][j]
	return D

def circle2circleDist(x1, y1, r1, x2, y2, r2, in12, in21): # in12 = is shape 1 inside shape 2
	#print ("circle2circleDist("+str(x1)+", "+str(y1)+", "+str(r1)+", "+str(x2)+", "+str(y2)
	#	+", "+str(r2)+", "+str(in12)+", "+str(in21)+")")
	if in12:
		return r2 - r1 - math.sqrt((x1-x2)**2+(y1-y2)**2)
	if in21:
		return r1 - r2 - math.sqrt((x1-x2)**2+(y1-y2)**2)
	else:
		return math.sqrt((x1-x2)**2+(y1-y2)**2) - r1 - r2

def circle2rectDist(xc, yc, r, xl, xr, yt, yb, in12, in21):
	#print ("circle2rectDist("+str(xc)+", "+str(yc)+", "+str(r)+", "+str(xl)+", "+str(xr)
	#	+", "+str(yt)+", "+str(yb)+", "+str(in12)+", "+str(in21)+")")

	#    |     |
	#  1 |  2  | 3
	# ___|_____|___
	#    |     |
	#  8 |     | 4
	# ___|_____|___
	#    |     |
	#  7 |  6  | 5
	#    |     |

	if in12: # circle in rect
		return min([xc-xl, xr-xc, yc-yt, yb-yc])-r
	if in21: # rect in circle
		return r-math.sqrt(max(xc-xl,xr-xc)**2+max(yc-yt,yb-yc)**2)
	if xc < xl and yc < yt: # 1
		return math.sqrt((xc-xl)**2+(yc-yt)**2)-r
	if xc > xr and yc < yt: # 3
		return math.sqrt((xc-xr)**2+(yc-yt)**2)-r
	if xc > xr and yc > yb: # 5
		return math.sqrt((xc-xr)**2+(yc-yb)**2)-r
	if xc < xl and yc > yb: # 7
		return math.sqrt((xc-xl)**2+(yc-yb)**2)-r
	if yc < yt: # 2
		return yt-yc-r
	if xc > xr: # 4
		return xc-xr-r
	if yc > yb: # 6
		return yc-yb-r
	if xc < xl: # 8
		return xl-xc-r

def rect2rectDist(xl1, xr1, yt1, yb1, xl2, xr2, yt2, yb2, in12, in21):
	#print ("rect2rectDist("+str(xl1)+", "+str(xr1)+", "+str(yt1)+", "+str(yb1)+", "+str(xl2)
	#	+", "+str(xr2)+", "+str(yt2)+", "+str(yb2)+", "+str(in12)+", "+str(in21)+")")
	if in12:
		return min([xl1-xl2, xr2-xr1, yt1-yt2, yb2-yb1])
	if in21:
		return min([xl2-xl1, xr1-xr2, yt2-yt1, yb1-yb2])
	if xr1 < xl2 and yb1 < yt2: # 1
		return math.sqrt((xr1-xl2)**2+(yb1-yb2)**2)
	if xl1 > xr2 and yb1 < yt2: # 3
		return math.sqrt((xl1-xr2)**2+(yb1-yt2)**2)
	if xl1 > xr2 and yt1 > yb2: # 5
		return math.sqrt((xl1-xr2)**2+(yt1-yb2)**2)
	if xr1 < xl2 and yt1 > yb2: # 7
		return math.sqrt((xr1-xl2)**2+(yt1-yb2)**2)
	if yb1 < yt2: # 2
		return yt2-yb1
	if xl1 > xr2: # 4
		return xl1-xr2
	if yt1 > yb2: # 6
		return yt1-yb2
	if xr1 < xl2: # 8
		return xl2-xr1

# import cv2, utils
# import cairo.test_cases as tc
# from encoder import simple
# from concepts import shapedist
# prog, shapes = simple.encode(tc.tc(13).draw())
# D = shapedist.distanceMatrix(shapes)