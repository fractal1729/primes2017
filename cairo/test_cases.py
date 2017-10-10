import cairo.tree as ct
from encoder import simple

def tc(i):
	pr = None
	if i == 1: # Two hughs
		pr = ct.Pr([ct.Sq(ct.Po((0.3, 0.3)), 0.2), ct.Sq(ct.Po((0.7, 0.7)), 0.2), ct.Ci(ct.Po((0.3, 0.3)), 0.05, (0,255,0)), ct.Ci(ct.Po((0.7, 0.7)), 0.05, (255,0,0))])
	if i == 2: # Red-in-black hugh
		pr = ct.Pr([ct.Sq(ct.Po((0.5,0.5)), 0.4), ct.Ci(ct.Po((0.5,0.5)), 0.1, (255,0,0))])
	if i == 3: # Blue-in-black hugh
		pr = ct.Pr([ct.Sq(ct.Po((0.5,0.5)), 0.4), ct.Ci(ct.Po((0.5,0.5)), 0.1, (0,0,255))])
	if i == 4: # Circle and rectangle in square
		pr = ct.Pr([ct.Sq(ct.Po((0.45,0.55)), 0.8), ct.Ci(ct.Po((0.2,0.3)),0.1,(255,0,0)), ct.Sq(ct.Po((0.5,0.7)),0.3,(0,255,0))])
	if i == 5: # Square in circle in square
		pr = ct.Pr([ct.Sq(ct.Po((0.5,0.5)), 0.8), ct.Ci(ct.Po((0.5,0.5)),0.3, (255, 0, 0)), ct.Sq(ct.Po((0.5,0.5)),0.35,(0,255,0))])
	if i == 6: # Sample face
		pr = ct.Pr([
			ct.Sq((0.5,0.5), 0.8),
			ct.Sq((0.3,0.3), 0.15, (255, 255, 255)),
			ct.Ci((0.3,0.3), 0.05, (0, 100, 255)),
			ct.Sq((0.7,0.3), 0.15, (0, 100, 255)),
			ct.Ci((0.7,0.3), 0.05, (255, 255, 255)),
			ct.Ci((0.5,0.5), 0.07, (255, 0, 0)),
			ct.Re((0.5,0.75), 0.5, 0.1, (0, 255, 0))
			])
	if i == 7: # Different shade of blue in black hugh
		pr = ct.Pr([ct.Sq(ct.Po((0.5,0.5)), 0.4), ct.Ci(ct.Po((0.5,0.5)), 0.1, (0,100,255))])
	if i == 8: # Lots of hughs and non-hughs
		pr = ct.Pr([
			ct.Sq((0.3, 0.3), 0.2, (0, 0, 0)),
			ct.Ci((0.3, 0.3), 0.05, (150, 150, 50)),
			ct.Sq((0.47, 0.82), 0.2, (50, 200, 60)),
			ct.Ci((0.48, 0.81), 0.04, (255, 0, 0)),
			ct.Sq((0.74, 0.53), 0.3, (100, 50, 255)),
			ct.Ci((0.72, 0.53), 0.1, (0, 0, 0)),
			ct.Sq((0.8, 0.15), 0.2, (0, 255, 0)),
			ct.Sq((0.8, 0.16), 0.1, (255, 0, 0)),
			ct.Ci((0.15, 0.8), 0.1, (60, 60, 60))
			])
	if i == 9: # Traffic light
		pr = ct.Pr([
			ct.Re((0.5, 0.5), 0.3, 0.9, (0, 0, 0)),
			ct.Ci((0.5, 0.2), 0.1, (0, 255, 0)),
			ct.Ci((0.5, 0.5), 0.1, (255, 255, 0)),
			ct.Ci((0.5, 0.8), 0.1, (255, 0, 0))
			])
	if i == 10: # Fancy traffic light
		pr = ct.Pr([
			ct.Re((0.5, 0.5), 0.4, 0.95, (0, 0, 0)),
			ct.Sq((0.5, 0.2), 0.25, (165, 42, 42)),
			ct.Ci((0.5, 0.2), 0.09, (0, 255, 0)),
			ct.Sq((0.5, 0.5), 0.25, (165, 42, 42)),
			ct.Ci((0.5, 0.5), 0.09, (255, 255, 0)),
			ct.Sq((0.5, 0.8), 0.25, (165, 42, 42)),
			ct.Ci((0.5, 0.8), 0.09, (255, 0, 0))
			])
	if i == 11:
		
	return pr
def test(i):
	return simple.encode(tc(i).draw(), True)