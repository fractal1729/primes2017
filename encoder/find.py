import cv2
import cairo.tree as ct
from concepts.objects import NotInstanceError
from encoder import simple
from concepts import objects
import cairo.test_cases as tc

def findHughsHardCode(shapes):
	hughs = []
	for shape in shapes:
		if(isinstance(shape.program, ct.Sq) and
			len(shape.children) == 1 and
			isinstance(shape.children[0].program, ct.Ci)):
			hughs.append(ct.Hugh(shape.program, shape.children[0].program))
	return hughs

def find(shapes, Obj):
	obj_list = []
	for shape in shapes:
		try:
			obj = Obj(shape)
			obj_list.append(obj)
		except NotInstanceError:
			pass
	return obj_list

def testTrafficLights(i):
	pix = tc.tc(i).draw()
	prog, shapes = simple.encode(pix)
	return find(shapes, objects.TrafficLight)