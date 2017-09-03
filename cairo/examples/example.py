import cairocffi as cairo

WIDTH = 256
HEIGHT = 256

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)
# with ctx:
# 	ctx.set_source_rgb(1, 1, 1)
# 	ctx.paint()

ctx.scale(WIDTH, HEIGHT)
ctx.set_line_width(0.01)

ctx.rectangle(0.1, 0.1, 0.2, 0.3)
ctx.set_source_rgb(0, 1, 0)
ctx.fill()

ctx.move_to(0.7, 0.7)
ctx.line_to(0.9, 0.7)
ctx.line_to(0.8, 0.8732)
ctx.close_path()
ctx.set_source_rgb(0, 1, 0)
ctx.fill()

surface.write_to_png('example.png')