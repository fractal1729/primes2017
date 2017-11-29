import cv2
import numpy as np
from concepts import features
from encoder import simple

n = 18 # n concepts
m = 5 # m examples for each concept

def trainingImages(): # returns images, classes
	images = []
	classes = []

	# total: m*n images

	for i in range(n):
		for j in range(m):
			filename = '{:02}'.format(i)+'-'+str(j)+'.png'
			img = cv2.imread('cairo/test_cases/svmdata/'+filename)
			images += [img]
			classes += [i]

	images = np.array(images)
	classes = np.array(classes)

	return images, classes

def walkThruImages():
	images, Y = trainingImages()
	for i in range(n*m):
		img = images[i]
		p,s = simple.encode(img)
		p.preview()

def writeCustomFeatures():
	images, Y = trainingImages()
	X = np.zeros((n*m, features.NUM_FEATURES))
	for i in range(n*m):
		img = images[i]
		p, s = simple.encode(img)
		X[i] = features.getFeatures(s)
		print str(i)+" done"
	np.save("learning/customfeatures", X)

def trainingCustomFeatures():
	X = np.load("learning/customfeatures.npy")
	Y = np.zeros((n*m))
	for i in range(n*m):
		Y[i] = i/m
	return X, Y

def trainingInceptionFeatures(): # returns X, Y
	X = np.zeros((n*m, 2048))
	for i in range(n):
		x = np.load('nn/inceptionfeatures/'+'{:02}'.format(i)+'.npy')
		for j in range(m):
			X[i*m+j] = x[j]

	Y = np.zeros((n*m))
	for i in range(n*m):
		Y[i] = i/m
	return X, Y

if __name__ == '__main__':
	writeCustomFeatures()