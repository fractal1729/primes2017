import cairocffi as cairo
import math

WIDTH = 256
HEIGHT = 256

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
cr = cairo.Context(surface)
cr.set_source_rgb(255, 255, 255)
cr.paint()

cr.scale(WIDTH, HEIGHT)
cr.set_line_width(0.01)

cr.set_source_rgb(0, 0, 0)
cr.rectangle(0.3, 0.3, 0.4, 0.4)
cr.fill()

cr.set_source_rgb(0, 0.3, 0)
cr.arc(0.5, 0.5, 0.1, 0, 2*math.pi)
cr.fill()

surface.write_to_png('cairo/examples/hugh.png')