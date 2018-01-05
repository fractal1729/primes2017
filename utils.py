import cv2

def previewWithIDs(prog, shapes, idcolor=(0,0,0)):
	imageb = prog.draw()
	image = imageb.copy() # i have to make a copy due to some bug in opencv...
	# see https://stackoverflow.com/questions/30249053/python-opencv-drawing-errors-after-manipulating-array-with-numpy
	# and https://stackoverflow.com/questions/23830618/python-opencv-typeerror-layout-of-the-output-array-incompatible-with-cvmat
	for i in range(len(shapes)):
		cv2.putText(image, str(i), (int(shapes[i].program.center.x.val*256)-5*len(str(i)), int(shapes[i].program.center.y.val*256)+5),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, idcolor, 2)
	cv2.imshow("preview with IDs", image)
	cv2.waitKey(0)

def RGB2BGR(img):
	return img[:,:,[2,1,0]]

def BGR2RGB(img):
	return img[:,:,[2,1,0]]

def preview(img):
	cv2.imshow('preview', img)
	cv2.waitKey(0)

def pointDistance(a, b):
	ax = a.x.val
	ay = a.y.val
	bx = b.x.val
	by = b.y.val
	return ((a.x.val - b.x.val)**2 + (a.y.val - b.y.val)**2)**0.5

def isInside(shape1, shape2):
	s = shape1
	while(s != None):
		s = s.parent
		if s == shape2:
			return True
	return False

def syncSVMDataset(n, m):
	

# import utils, cv2
# from encoder import simple
# from concepts import align
# calc1 = cv2.imread('cairo/test_cases/calc1.png')
# prog, shapes = simple.encode(calc1)
# a=align.findCenterAlignments(shapes)
# a
# utils.drawWithIDs(prog, shapes)