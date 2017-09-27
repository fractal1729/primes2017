import numpy as np
import cairo.tree as ct
import scipy.stats
import sys

def generateRow(p1=None, p2=None, n=None, sigma=0.005): # two endpoints and number of points in total (including endpoints)
	# ct.Point() is not the default in the function because I might want to specify a non-uniform distribution for this later.
	# Also sigma needs to be adjusted to the optimal value.
	if not p1: p1 = ct.Point()
	if not p2: p2 = ct.Point()
	if n < 3: n = 3
	xstep = (p2.x.val - p1.x.val)/(n-1)
	ystep = (p2.y.val - p1.y.val)/(n-1)
	row = ct.PointSet()
	sigma = 0.005 # needs to be adjusted to the optimal value, this seems reasonable for now
	for i in range(n):
		row.addPoint(perturbPoint(ct.Po((p1.x.val + i*xstep, p1.y.val + i*ystep)), sigma))
	return row, p1, p2, n

def perturbPoint(p, sigma):
	x = p.x.val
	y = p.y.val
	# Instead of using a truncnorm distribution here, I'm just taking a normal distribution and
	# manually chopping off the edges, setting anything outside to one of the boundary values
	# instead of resampling.  This may not be mathematically accurate but it's probably perfectly
	# fine in my case where the perturbations are all really small.
	x1 = np.random.normal(x, sigma)
	if x1 < 0: x1 = 0
	if x1 > 1: x1 = 1
	y1 = np.random.normal(y, sigma)
	if y1 < 0: y1 = 0
	if y1 > 1: y1 = 1
	return ct.Po((x1, y1))

def guessRow(points, num_guesses=100):
	bestguess = None
	bestp1 = None
	bestp2 = None
	bestn = None
	mindist = float("inf")
	for i in range(num_guesses):
		guess, p1, p2, n = generateRow(n=points.size())
		dist = hd(points, guess)
		if dist < mindist:
			bestguess = guess
			bestp1 = p1
			bestp2 = p2
			bestn = n
			mindist = dist
	return bestguess, bestp1, bestp2, bestn, mindist

def hd(P1, P2): # find the distance between two point sets
	# The naive solution: Hausdorff distance
	h12 = 0
	for i in range(P1.size()):
		a = P1.getPoint(i)
		d = sys.maxint
		for j in range(P2.size()):
			b = P2.getPoint(j)
			d = min(d, pointDistance(a,b))
		h12 = max(h12, d)
	h21 = 0
	for i in range(P2.size()):
		a = P2.getPoint(i)
		d = sys.maxint
		for j in range(P1.size()):
			b = P1.getPoint(j)
			d = min(d, pointDistance(a,b))
		h21 = max(h21, d)
	return max(h12, h21)

def pointDistance(a, b):
	ax = a.x.val
	ay = a.y.val
	bx = b.x.val
	by = b.y.val
	return ((a.x.val - b.x.val)**2 + (a.y.val - b.y.val)**2)**0.5

def previewPointSets(P1, P2):
	pr = ct.Pr([])
	for p in P1.points:
		pr.addComponent(ct.Ci(p, 0.01, (0, 0, 255), True))
	for p in P2.points:
		pr.addComponent(ct.Ci(p, 0.01, (255, 0, 0), True))
	pr.preview()

def test(num_tests, num_guesses=100, preview=True, n=5):
	distances = []
	for i in range(num_tests):
		points = generateRow(n=n)
		guess = guessRow(points[0], num_guesses)
		distances.append(guess[4])
		if preview: previewPointSets(points[0], guess[0])
	return distances