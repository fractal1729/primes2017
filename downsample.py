import numpy as numpy
from scipy import ndimagep
from PIL import Image
import numpy as np

def block_mean(ar, fact):
	assert isinstance(fact, int), type(fact)
	sx, sy = ar.shape
	X, Y = np.ogrid[0:sx,0:sy]
	regions = sy/fact * (X/fact) + (Y/fact)
	res = ndimage.mean(ar, labels=regions, index=np.arange(regions.max() + 1))
	res.shape = (sx/fact, sy/fact)
	return res

def downsample(img, factor): # input image as 2D nparray
	

if __name__ == "__main__":
	sample = np.array(Image.open("./images/SampleImage.png").convert('L'))
