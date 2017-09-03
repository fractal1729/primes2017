import rendermp, mptree
import numpy as np
import random
import sys

batch_size = 100
num_train_batches = 100 # 10000 trainig
num_test_batches = 20 # 2000 test
num_train = num_train_batches*batch_size
num_test = num_test_batches*batch_size

X_train = np.zeros((num_train, rendermp.CANVAS_SIZE, rendermp.CANVAS_SIZE))
X_test = np.zeros((num_test, rendermp.CANVAS_SIZE, rendermp.CANVAS_SIZE))
y_train = np.zeros((num_train))
y_test = np.zeros((num_test))

def go():
	for i in range(num_train_batches): # prep training data
		mpsrcs = ['']*batch_size
		for j in range(batch_size):
			shape = random.randint(0,1)
			if shape == 0: # circle
				mpsrcs[j] = mptree.Draw(mptree.Circle()).tocode()
			if shape == 1: # square
				mpsrcs[j] = mptree.Draw(mptree.Square()).tocode()
			y_train[i*batch_size+j] = shape
		images = rendermp.renderImages(mpsrcs)
		for j in range(batch_size):
			X_train[i*batch_size+j] = images[j]
		sys.__stdout__.write("Building training dataset.................."+str(i*batch_size)+"/"+str(num_train)+" COMPLETE         \r",)

	print "Training dataset successfully built!"

	for i in range(num_test_batches): # prep training data
		mpsrcs = ['']*batch_size
		for j in range(batch_size):
			shape = random.randint(0,1)
			if shape == 0: # circle
				mpsrcs[j] = mptree.Draw(mptree.Circle()).tocode()
			if shape == 1: # square
				mpsrcs[j] = mptree.Draw(mptree.Square()).tocode()
			y_test[i*batch_size+j] = shape
		images = rendermp.renderImages(mpsrcs)
		for j in range(batch_size):
			X_test[i*batch_size+j] = images[j]
		sys.__stdout__.write("Building test dataset.................."+str(i*batch_size)+"/"+str(num_test)+" COMPLETE         \r",)

	print "Test dataset successfully built!"

	print "Saving data..."
	data = np.array([X_train, X_test, y_train, y_test])
	np.save("data", data)
	print "Data successfully saved.  Ending program."