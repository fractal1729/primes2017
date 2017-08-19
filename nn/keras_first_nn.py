# following http://machinelearningmastery.com/tutorial-first-neural-network-python-keras/

from keras.models import Sequential
from keras.layers import Dense
import numpy

# fix random seed for reproducibility
numpy.random.seed(7)

print "loading pima indians dataset...", # load pima indians dataset
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
print " done."

print "splitting data...", # split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
print " done."

print "creating model...", # create model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
print " done."

print "compiling model...", # compile model
model.compile(loss='binary_crossentropy', optimizer='adam',
	metrics=['accuracy'])
print " done."

print "fitting model...", # fit the model; this is where the work is done
model.fit(X, Y, epochs=150, batch_size=10)
print " done."

print "evaluating model...", # evaluate the model
scores = model.evaluate(X, Y)
print model.metrics_names[1], scores[1]*100
print " done."