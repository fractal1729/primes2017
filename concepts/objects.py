import cairo.tree as ct
from encoder import simple
import sys
import utils

class NotInstanceError(Exception):
	pass

def check(statement, checkid='-1'):
	if not statement:
		raise NotInstanceError(checkid)

class Hugh():

# Hugh
#  |-> square (rootShape)
#       |-> circle

	def __init__(self, rootShape, cp=''): # cp = checkprefix
		try:
			check(isinstance(rootShape.program, ct.Sq), cp+'0')
			self.rootShape = rootShape # root is a square in Hugh
			self.square = self.rootShape
			check(len(rootShape.children) == 1, cp+'1')
			check(isinstance(rootShape.children[0].program, ct.Ci), cp+'2')
			self.circle = rootShape.children[0]
			check(len(self.circle.children) == 0, cp+'3')
			check(utils.pointDistance(self.circle.program.center, self.square.program.center) <= 0.25*self.square.program.sidelength.val, cp+'4')
			check(self.circle.program.radius.val <= 0.85*self.square.program.sidelength.val
				and self.circle.program.radius.val >= 0.25*self.square.program.sidelength.val, cp+'5')

		except NotInstanceError as e:
			print e.args[0]
			raise sys.exc_info()

class TrafficLight():

# TrafficLight
#  |-> rect (rootShape)
#  |-{ thirds }
#       |-> topCircle (thirds[0][0])
#       |-> midCircle (thirds[1][0])
#       |-> botCircle (thirds[2][0])

	def __init__(self, rootShape, cp=''):
		try:
			check(isinstance(rootShape.program, ct.Re), cp+'0')
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
				check(isinstance(c.program, ct.Ci), cp+'3')
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

class FancyTrafficLight():

# FTL
#  |-> rect (rootShape)
#  |-{ thirds }
#       |-- topHugh (thirds[0][0])
#       |-- midHugh (thirds[1][0])
#       |-- botHugh (thirds[2][0])

	def __init__(self, rootShape, cp=''):
		try:
			check(isinstance(rootShape.program, ct.Re), cp+'0')
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