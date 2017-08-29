import random
import math
from scipy.stats import truncnorm
import rendermp, config

# Notes:
# Might want to make code an attribute so that it can be accessed multiple
# times without having to recompute each time.

CANVAS_SIZE = config.CANVAS_SIZE
NUMERIC_SCALE_FACTOR = config.NUMERIC_SCALE_FACTOR
NUMERIC_MAX_VALUE = int(math.floor(float(CANVAS_SIZE-1)/NUMERIC_SCALE_FACTOR))
NUMERIC_MIN_VALUE = 1

class Program: # currently set up to draw two lines randomly on the 50x50 canvas
	def __init__(self, commands=None):
		if commands: self.commands = commands
		else: self.commands = [Draw(LinePath())]

	def mutate(self):
		for command in self.commands:
			command.mutate()

	def tocode(self):
		code = self.commands[0].tocode()
		for i in range(1, len(self.commands)):
			code += "\n"+self.commands[i].tocode()
		return code

class Draw:
	def __init__(self, path=None):
		if path: self.path = path # Path
		else:
			self.path = LinePath() # generate random LinePath
			#self.path = Circle() # generate random Circle

	def mutate(self):
		self.path.mutate()

	def tocode(self):
		return "draw "+self.path.tocode()+";"

class Fill:
	def __init__(self, path=None):
		if path: self.path = path # Path
		else:
			#self.path = LinePath() # generate random LinePath
			self.path = Circle() # generate random Circle

	def mutate(self):
		self.path.mutate()

	def tocode(self):
		return "fill "+self.path.tocode()+";"

class Circle():
	def __init__(self, center=None, radius=None, color=None):
		if center: self.center = center
		if not center: self.center = Pair()
		
		if radius: self.radius = radius
		if not radius:
			xbound = min(self.center.x.val,CANVAS_SIZE-self.center.x.val)
			ybound = min(self.center.y.val,CANVAS_SIZE-self.center.y.val)
			self.radius = Numeric(maxVal=min(xbound, ybound))

		if color: self.color = color
		if not color: self.color = "black"

	def mutate(self):
		self.center.mutate()
		self.radius.mutate()
		# no mutation of color

	def tocode(self):
		return "fullcircle scaled "+self.radius.tocode()+" shifted "+self.center.tocode()+" withcolor "+self.color

class Square():
	def __init__(self, bottom_left=None, sidelength=None):
		if sidelength: self.sidelength = sidelength
		else: self.sidelength = Numeric(maxVal=NUMERIC_MAX_VALUE-1)

		if bottom_left: self.bottom_left = bottom_left
		else:
			self.bottom_left = Pair(Numeric(maxVal=NUMERIC_MAX_VALUE-self.sidelength.val),
				Numeric(maxVal=NUMERIC_MAX_VALUE-self.sidelength.val))

	def mutate(self):
		self.sidelength.mutate()
		self.bottom_left.mutate()

	def tocode(self):
		bottom_right = Pair(Numeric(val=(self.bottom_left.x.val+self.sidelength.val)), Numeric(val=self.bottom_left.y.val))
		top_left = Pair(Numeric(val=self.bottom_left.x.val), Numeric(val=(self.bottom_left.y.val+self.sidelength.val)))
		top_right = Pair(Numeric(val=(self.bottom_left.x.val+self.sidelength.val)), Numeric(val=(self.bottom_left.y.val+self.sidelength.val)))
		return self.bottom_left.tocode()+"--"+bottom_right.tocode()+"--"+top_right.tocode()+"--"+top_left.tocode()+"--cycle"

class LinePath(): # currently this path is lines-only, no Bezier curves
	def __init__(self, pairs=None):
		if pairs: self.pairs = pairs # array of Pair objects
		else: self.pairs = [Pair(), Pair()] # generate random pair of Pairs

	def mutate(self):
		for pair in self.pairs:
			pair.mutate()
		# for now, I am only dealing with two-point paths, but if
		# I used longer paths I would have to add a mutation that
		# can make the path longer

	def tocode(self):
		code = self.pairs[0].tocode()
		for i in range(1, len(self.pairs)):
			code += "--"+self.pairs[i].tocode()
		return code

class Pair:
	def __init__(self, x=None, y=None):
		if x: self.x = x # Numeric
		if not x: self.x = Numeric() # generate random Numeric

		if y: self.y = y # Numeric
		if not y: self.y = Numeric() # generate random Numeric

	def mutate(self):
		self.x.mutate()
		self.y.mutate()

	def tocode(self):
		return "("+self.x.tocode()+","+self.y.tocode()+")"

class Numeric:

	P_SIGMA_RESET = config.P_SIGMA_RESET # number should be tweaked
	SIGMA_DECAY_FACTOR = config.SIGMA_DECAY_FACTOR # number should be tweaked
	SIGMA_RESET_VAL = config.SIGMA_RESET_VALUE

	def __init__(self, val=None, minVal=NUMERIC_MIN_VALUE, maxVal=NUMERIC_MAX_VALUE, sigma=None):
		if val: self.val = val
		else: self.val = random.randint(minVal, maxVal) # generate random value in range
		self.minVal = minVal
		self.maxVal = maxVal
		#self.sigma_reset_val = (float)(maxVal-minVal)/4 # this is pretty arbitrary
		self.sigma_reset_val = self.SIGMA_RESET_VAL
		if sigma: self.sigma = (float)(sigma)
		else: self.sigma = self.sigma_reset_val
		self.time_absolute = 0
		self.time_since_reset = 0

	def mutate(self):
		self.mutate_sigma()
		self.val = (int)(truncnorm.rvs(((float)(self.minVal-self.val))/((float)(self.sigma)),
			((float)(self.maxVal-self.val))/((float)(self.sigma)), loc=self.val, scale=self.sigma))

	def snapTo(self, val, a): # snaps val to the nearest multiple of a; this function is no longer used
		return int(a*round(float(val)/a))

	def mutate_sigma(self):
		self.time_absolute += 1
		self.time_since_reset += 1
		p = random.random()
		if p < self.P_SIGMA_RESET: # reset sigma
			self.sigma = self.sigma_reset_val
			self.time_since_reset += 1
		else: # decay sigma
			self.sigma = self.SIGMA_DECAY_FACTOR

	def tocode(self):
		return str(self.val*NUMERIC_SCALE_FACTOR)

# if __name__ == "__main__":
# 	d = Draw()
# 	print d.tocode()
# 	f = Fill()
# 	print f.tocode()