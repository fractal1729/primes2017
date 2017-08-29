import rendermp, mptree
import numpy as np
import random
import sys

num_train = 10000
num_test = 2000

X_train = np.zeros((num_train, rendermp.CANVAS_SIZE, rendermp.CANVAS_SIZE))
X_test = np.zeros((num_test, rendermp.CANVAS_SIZE, rendermp.CANVAS_SIZE))
y_train = np.zeros((num_train))
y_test = np.zeros((num_test))

for i in range(num_train): # prep training data
	shape = random.randint(0,1)
	if shape == 0: # circle
		img = rendermp.renderImage(mptree.Draw(mptree.Circle()).tocode())
		X_train[i] = img
	if shape == 1: # square
		img = rendermp.renderImage(mptree.Draw(mptree.Square()).tocode())
		X_train[i] = img
	y_train[i] = shape
	sys.__stdout__.write("Building training dataset:                  "+str(i)+"/"+str(num_train)+" COMPLETE         \r",)

print "Training dataset successfully built!"

for i in range(num_test):
	shape = random.randint(0,1)
	if shape == 0: # circle
		img = rendermp.renderImage(mptree.Draw(mptree.Circle()).tocode())
		X_test[i] = img
	if shape == 1: # square
		img = rendermp.renderImage(mptree.Draw(mptree.Square()).tocode())
		X_test[i] = img
	y_test[i] = shape
	sys.__stdout__.write("Building test dataset:                    "+str(i)+"/"+str(num_test)+" COMPLETE         \r",)

print "Test dataset successfully built!"
print "Saving data..."
data = np.array([X_train, X_test, y_train, y_test])
np.save("data", data)
print "Data successfully saved.  Ending program."