import random
from scipy.stats import truncnorm

# Notes:
# Might want to make code an attribute so that it can be accessed multiple
# times without having to recompute each time.

CANVAS_SIZE = 50
NUMERIC_MAX_VALUE = CANVAS_SIZE-1
NUMERIC_MIN_VALUE = 1

class Program: # currently set up to draw a single black circle randomly on the 50x50 canvas
	def __init__(self, commands=None):
		if commands: self.commands = commands
		else: self.commands = [Draw(), Draw()]

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
			self.radius = Numeric(minVal=1, maxVal=min(xbound, ybound))

		if color: self.color = color
		if not color: self.color = "black"

	def mutate(self):
		self.center.mutate()
		self.radius.mutate()
		# no mutation of color

	def tocode(self):
		return "fullcircle scaled "+self.radius.tocode()+" shifted "+self.center.tocode()+" withcolor "+self.color

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
	def __init__(self, val=None, minVal=NUMERIC_MIN_VALUE, maxVal=NUMERIC_MAX_VALUE, sigma=None):
		if val: self.val = val
		else: self.val = random.randint(minVal, maxVal) # generate random value in range
		self.minVal = minVal
		self.maxVal = maxVal
		if sigma: self.sigma = sigma
		else: self.sigma = (float)(maxVal-minVal)/10 # this is pretty arbitrary
		self.time = 0

	def mutate(self):
		# self.time++
		# self.sigma =  # stochastic stdev decay
		self.val = truncnorm.rvs(((float)(self.minVal-self.val))/((float)(self.sigma)),
			((float)(self.maxVal-self.val))/((float)(self.sigma)), loc=self.val, scale=self.sigma)

	def tocode(self):
		return str(self.val)

# if __name__ == "__main__":
# 	d = Draw()
# 	print d.tocode()
# 	f = Fill()
# 	print f.tocode()