import cairo.tree as ct
from encoder import simple
import sys
import utils

#####################
# OBJECT GENERATORS #
#####################


def generateUpHughs(num):
	pixels = []
	programs = []
	params = []
	for i in range(num):
		sidelength = ct.Nu(minVal=0.2, maxVal=0.9)
		sqX = ct.Nu(minVal=sidelength.val/2, maxVal=1-sidelength.val/2)
		sqY = ct.Nu(minVal=sidelength.val/2, maxVal=1-sidelength.val/2)
		square = ct.Sq(ct.Po((sqX, sqY)), sidelength, (0, 0, 0))
		radius = ct.Nu(minVal=sidelength.val*0.1, maxVal=sidelength.val*0.2)
		ciX = ct.Nu(minVal=sqX.val-sidelength.val/2+radius.val, maxVal=sqX.val+sidelength.val/2-radius.val)
		ciY = ct.Nu(minVal=sqY.val-sidelength.val/2+radius.val, maxVal=sqY.val-radius.val) # this is the diff line
		circle = ct.Ci(ct.Po((ciX, ciY)), radius, (255, 0, 0))
		prog = ct.Pr([square, circle])
		programs.append(prog)
		pixels.append(prog.draw())
		params.append(prog.flatParams())
	return programs, pixels, params

def generateDownHughs(num):
	pixels = []
	programs = []
	params = []
	for i in range(num):
		sidelength = ct.Nu(minVal=0.2, maxVal=0.9)
		sqX = ct.Nu(minVal=sidelength.val/2, maxVal=1-sidelength.val/2)
		sqY = ct.Nu(minVal=sidelength.val/2, maxVal=1-sidelength.val/2)
		square = ct.Sq(ct.Po((sqX, sqY)), sidelength, (0, 0, 0))
		radius = ct.Nu(minVal=sidelength.val*0.1, maxVal=sidelength.val*0.2)
		ciX = ct.Nu(minVal=sqX.val-sidelength.val/2+radius.val, maxVal=sqX.val+sidelength.val/2-radius.val)
		ciY = ct.Nu(minVal=sqY.val+radius.val, maxVal=sqY.val+sidelength.val/2-radius.val) # this is the diff line
		circle = ct.Ci(ct.Po((ciX, ciY)), radius, (255, 0, 0))
		prog = ct.Pr([square, circle])
		programs.append(prog)
		pixels.append(prog.draw())
		params.append(prog.flatParams())
	return programs, pixels, params

#####################
#  OBJECT CHECKERS  #
#####################

class NotInstanceError(Exception):
	pass

def check(statement, checkid='-1'):
	if not statement:
		raise NotInstanceError(checkid)

class Hugh():

# Hugh
#  |-> square (rootShape)
#       |-> circle

	def __init__(self, rootShape, cp='', generateNew=False): # cp = checkprefix
		if not generateNew:
			try:
				check(rootShape.type == "sq", cp+'0')
				self.rootShape = rootShape # root is a square in Hugh
				self.square = self.rootShape
				check(len(rootShape.children) == 1, cp+'1')
				check(rootShape.children[0].type == "ci", cp+'2')
				self.circle = rootShape.children[0]
				check(len(self.circle.children) == 0, cp+'3')
				# check(utils.pointDistance(self.circle.program.center, self.square.program.center) <= 0.25*self.square.program.sidelength.val, cp+'4')
				check(self.circle.program.radius.val <= 0.45*self.square.program.sidelength.val
					and self.circle.program.radius.val >= 0.08*self.square.program.sidelength.val, cp+'5')

			except NotInstanceError as e:
				print e.args[0]
				raise sys.exc_info()

	def flatParams(self): # a flat array of all the parameters?
		return self.square.flatParams() + self.circle.flatParams()

class TrafficLight():

# TrafficLight
#  |-> rect (rootShape)
#  |-{ thirds }
#       |-> topCircle (thirds[0][0])
#       |-> midCircle (thirds[1][0])
#       |-> botCircle (thirds[2][0])

	def __init__(self, rootShape, cp=''):
		try:
			check(rootShape.type == "re", cp+'0')
			self.rootShape = rootShape
			self.rect = rootShape
			aspect_ratio = self.rect.program.height.val/self.rect.program.width.val
			check(aspect_ratio >= 1.4 and aspect_ratio <= 4, cp+'1')
			check(len(self.rect.children) == 3, cp+'2')
			thirds = [[], [], []] # top, mid, bottom
			rectX = self.rect.program.center.x.val
			rectY = self.rect.program.center.y.val
			rectTop = rectY - self.rect.program.height.val/2
			rectBot = rectY + self.rect.program.height.val/2
			rectLeft = rectX - self.rect.program.width.val/2
			rectRight = rectX + self.rect.program.width.val/2
			for c in self.rect.children:
				check(c.type == "ci", cp+'3')
				check(len(c.children) == 0, cp+'4')
				in_top_third = (c.program.center.y.val + c.program.radius.val <= (2*rectTop + rectBot)/3)
				in_mid_third = (c.program.center.y.val - c.program.radius.val >= (2*rectTop + rectBot)/3
					and c.program.center.y.val + c.program.radius.val <= (rectTop + 2*rectBot)/3)
				in_bot_third = (c.program.center.y.val - c.program.radius.val >= (rectTop + 2*rectBot)/3)
				if in_top_third: thirds[0].append(c)
				if in_mid_third: thirds[1].append(c)
				if in_bot_third: thirds[2].append(c)
			check(len(thirds[0]) == 1 and len(thirds[1]) == 1 and len(thirds[2]) == 1, cp+'5')
			self.topCircle = thirds[0][0]
			self.midCircle = thirds[1][0]
			self.botCircle = thirds[2][0]

		except NotInstanceError as e:
			#print e.args[0]
			raise sys.exc_info()

	def flatParams(self):
		return (self.rect.flatParams() + self.topCircle.flatParams()
			+ self.midCircle.flatParams() + self.botCircle.flatParams())

class FancyTrafficLight():

# FTL
#  |-> rect (rootShape)
#  |-{ thirds }
#       |-- topHugh (thirds[0][0])
#       |-- midHugh (thirds[1][0])
#       |-- botHugh (thirds[2][0])

	def __init__(self, rootShape, cp=''):
		try:
			check(rootShape.type == "re", cp+'0')
			self.rootShape = rootShape
			self.rect = rootShape
			aspect_ratio = self.rect.program.height.val/self.rect.program.width.val
			check(aspect_ratio >= 1.4 and aspect_ratio <= 4, cp+'1')
			check(len(self.rect.children) == 3, cp+'2')
			thirds = [[], [], []]
			rectX = self.rect.program.center.x.val
			rectY = self.rect.program.center.y.val
			rectTop = rectY - self.rect.program.height.val/2
			rectBot = rectY + self.rect.program.height.val/2
			rectLeft = rectX - self.rect.program.width.val/2
			rectRight = rectX + self.rect.program.width.val/2
			for h in self.rect.children:
				hugh = Hugh(h, cp+'3-')
				ctrY = hugh.square.program.center.y.val
				sl = hugh.square.program.sidelength.val
				in_top_third = (ctrY + 0.5*sl <= (2*rectTop + rectBot)/3)
				in_mid_third = (ctrY - 0.5*sl >= (2*rectTop + rectBot)/3 and ctrY + 0.5*sl <= (rectTop + 2*rectBot)/3)
				in_bot_third = (ctrY - 0.5*sl >= (rectTop + 2*rectBot)/3)
				if in_top_third: thirds[0].append(hugh)
				if in_mid_third: thirds[1].append(hugh)
				if in_bot_third: thirds[2].append(hugh)
			check(len(thirds[0]) == 1 and len(thirds[1]) == 1 and len(thirds[2]) == 1, cp+'4')
			self.topHugh = thirds[0][0]
			self.midHugh = thirds[1][0]
			self.botHugh = thirds[2][0]

		except NotInstanceError as e:
			#print e.args[0]
			raise sys.exc_info()

	def flatParams(self):
		return (self.rect.flatParams() + self.topHugh.flatParams()
			+ self.midHugh.flatParams() + self.botHugh.flatParams())

################

# EXPERIMENT TO TEST EXCEPTIONS
# Conclusion: it works.

# def foo():
# 	raise NotInstanceError()

# def bar():
# 	try:
# 		foo()
# 	except NotInstanceError:
# 		print "Excepted NotInstanceError in bar"
# 		raise sys.exc_info()

# def far():
# 	try:
# 		bar()
# 	except NotInstanceError:
# 		print "Excepted NotInstanceError in far"