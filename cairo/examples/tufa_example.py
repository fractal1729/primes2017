import math
import cairocffi as cairo

WIDTH = 256
HEIGHT = 256

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
cr = cairo.Context(surface)
with cr:
	cr.set_source_rgb(255, 255, 255)
	cr.paint()

cr.scale(WIDTH, HEIGHT)
cr.set_line_width(0.01)

cr.set_source_rgb(0, 255, 0)
cr.rectangle(0.35, 0.5, 0.3, 0.3)
cr.fill()

cr.set_source_rgb(255, 0, 0)
cr.arc(0.35, 0.5, 0.1, 0, 2*math.pi)
cr.fill()

cr.arc(0.65, 0.5, 0.1, 0, 2*math.pi)
cr.fill()

surface.write_to_png('cairo/examples/tufa_example.png')