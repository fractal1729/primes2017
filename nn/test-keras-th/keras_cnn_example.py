# Following https://elitedatascience.com/keras-tutorial-deep-learning-in-python
# unfinished due to the tutorial not working for Keras 2

########## Step 3: IMPORT LIBRARIES AND MODULES ##########

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from matplotlib import pyplot as plt

np.random.seed(123) # for reproducibility

########## Step 4: LOAD DATA FROM MNIST ##########

# Load pre-shuffled MNIST data into train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()
# print X_train.shape
# # (60000, 28, 28)

# plt.imshow(X_train[0])
# plt.show()

########## Step 5: PREPROCESS INPUT DATA ##########

X_train = X_train.reshape(X_train.shape[0], 1, 28, 28)
X_test = X_test.reshape(X_test.shape[0], 1, 28, 28)

# print X_train.shape
# # (60000, 1, 28, 28)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255.0
X_test /= 255.0

########## Step 6: PREPROCESS CLASS LABELS ##########

# Convert 1-dimensional class arrays to 10-dimensional
# matrices
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)

# print Y_train.shape

########## Step 7: DEFINE MODEL ARCHITECTURE ##########

model = Sequential()
model.add(Convolution2D(32, 3, 3, activation='relu',
	input_shape=(1,28,28)))

print model.output_shape
# (None, 32, 26, 26)