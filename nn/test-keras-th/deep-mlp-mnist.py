from keras.datasets import mnist # subroutines for fetching the MNIST dataset
from keras.models import Model # basic class for specifying and training a neural network
from keras.layers import Input, Dense # the two types of neural network layer we will be using
from keras.utils import np_utils # utilities for one-hot encoding of ground truth values

# HYPERPARAMETERS
# For the purposes of this tutorial, we will stick to using some sensible values, but keep in
# mind that properly training them is a significant issue, which will be addressed more properly
# in a future tutorial.

batch_size = 128 # in each iteration, we consider 128 training examples at once
num_epochs = 20 # we iterate twenty times over the entire training set
hidden_size = 512 # there will be 512 neurons in both hidden layers

num_train = 60000 # there are 60000 training examples in MNIST
num_test = 10000 # there are 10000 test examples in MNIST

height, width, depth = 28, 28, 1 # MNIST images are 28x28 and greyscale
num_classes = 10 # there are 10 classes (1 per digit)

(X_train, y_train), (X_test, y_test) = mnist.load_data() # fetch MNIST data
X_train = X_train.reshape(num_train, height * width)
X_test = X_test.reshape(num_test, height * width) # flatten data to 1D
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255 # normalize to [0, 1]
X_test /= 255

Y_train = np_utils.to_categorical(y_train, num_classes) # one-hot encode the labels
Y_test = np_utils.to_categorical(y_test, num_classes)

inp = Input(shape=(height * width,)) # our input is a 1D vector of size 784
hidden_1 = Dense(hidden_size, activation='relu')(inp) # first hidden ReLU layer
hidden_2 = Dense(hidden_size, activation='relu')(hidden_1) # second hidden ReLU layer
out = Dense(num_classes, activation='softmax')(hidden_2) # output softmax layer

model = Model(inputs=inp, outputs=out) # to define a model just specify its input and output layers

# As our classes are balanced (there is an equal amount of handwritten digits across all ten classes),
# an appropriate metric to report is the accuracy; the proportion of the inputs classified correctly.
# Note to self: look into what metrics are good if the data is not balanced.
model.compile(loss='categorical_crossentropy', #using the cross-entropy loss function
	optimizer='adam', # using the Adam optimizer
	metrics=['accuracy']) # reporting the accuracy

model.fit(X_train, Y_train, # train the model using the training set...
	batch_size=batch_size, epochs=num_epochs,
	verbose=1, validation_split=0.1) # ...holding out 10% of the data for validation
model.evaluate(X_test, Y_test, verbose=1) # evaluate the trained model on the test set
