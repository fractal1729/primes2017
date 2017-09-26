import cv2
import cairo.tree as ct

def findHughs(shapes):
	hughs = []
	for shape in shapes:
		if(isinstance(shape.program, ct.Sq) and
			len(shape.children) == 1 and
			isinstance(shape.children[0].program, ct.Ci)):
			hughs.append(ct.Hugh(shape.program, shape.children[0].program))
	return hughs

def alltrue(tests):
	for t in tests:
		if not t: return False
	return True