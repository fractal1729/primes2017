import cv2

def RGB2BGR(img):
	return img[:,:,[2,1,0]]

def BGR2RGB(img):
	return img[:,:,[2,1,0]]

def preview(img):
	cv2.imshow('preview', img)
	cv2.waitKey(0)