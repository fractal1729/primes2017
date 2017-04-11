import genmp, rendermp, mptree, compare
import re
import datetime, time
import numpy as numpy
import matplotlib.pyplot as plt
import sys

plt.subplot(1,2,1)
plt.imshow(rendermp.renderImage("fill fullcircle scaled 11 shifted (30,20) withcolor black;"), cmap="gray")
plt.title("Best randomly generated\ncandidate")
plt.subplot(1,2,2)
plt.imshow(rendermp.renderImage("fill fullcircle scaled 12 shifted (30,20) withcolor black;"), cmap="gray")
plt.title("Original image")
plt.show()