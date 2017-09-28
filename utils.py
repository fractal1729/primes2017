import cv2

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