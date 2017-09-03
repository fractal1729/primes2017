import cairocffi as cairo

WIDTH = 256
HEIGHT = 256

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
cr = cairo.Context(surface)
cr.set_source_rgb(255, 255, 255)
cr.paint()
cr.set_source_rgb(0, 0, 0)

cr.scale(WIDTH, HEIGHT)
cr.set_line_width(0.01)

cr.move_to(0.1, 0.1)
cr.line_to(0.8, 0.7)
cr.stroke()

cr.move_to(0.9, 0.2)
cr.line_to(0.2, 0.5)
cr.stroke()

surface.write_to_png('cairo/examples/two_lines_cross.png')