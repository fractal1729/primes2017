import cairo.tree as ct
from encoder import simple
import sys

class NotInstanceError(Exception):
	pass

def check(statement):
	if not statement:
		raise NotInstanceError()

class Hugh():

	def __init__(self, rootShape):
		try:
			check(isinstance(rootShape.program, ct.Sq))
			self.rootShape = rootShape # root is a square in Hugh
			self.square = self.rootShape
			check(len(rootShape.children) == 1)
			check(isinstance(rootShape.children[0].program, ct.Ci))
			self.circle = rootShape.children[0]
			check(len(self.circle.children) == 0)

		except NotInstanceError:
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