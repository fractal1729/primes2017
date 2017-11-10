import numpy as np
import random
from concepts import shapeutils
import cv2
import Queue # https://docs.python.org/2/library/queue.html
import copy
from scipy.cluster.hierarchy import fclusterdata

def hierarchicalCluster(shapes):
	D = shapeutils.distanceMatrix(shapes)
	def dist(a, b):
		return D[a[0]][b[0]]
	ids = [[i] for i in range(len(shapes))]
	fclust = fclusterdata(ids, 0.07, metric=dist)
	return fclust

def neighbors(shapes, threshold=0.1):
	D = shapeutils.distanceMatrix(shapes)
	N = [[]]*len(shapes)
	for i in range(len(shapes)):
		for j in range(len(shapes)):
			if i != j and D[i][j] <= threshold:
				N[i] = N[i]+[j]
	return N

def cluster(shapes, threshold=0.07): # if this ends up becoming too slow, implement adjacency list instead of matrix
	D = shapeutils.distanceMatrix(shapes)
	clusters = []
	assignments = [-1]*len(shapes)
	count = 0
	for i in range(len(shapes)):
		if assignments[i] == -1:
			cluster = set()
			q = Queue.Queue()
			cluster.add(shapes[i])
			q.put(i)
			while not q.empty():
				current = q.get()
				for j in range(len(shapes)):
					if current != j and D[current][j] <= threshold and assignments[j] == -1:
						assignments[j] = count
						cluster.add(shapes[j])
						q.put(j)
			cluster = list(cluster)
			clusters.append(cluster)
			count += 1
	return clusters, assignments

def previewClusters(shapes, threshold=0.07):
	clusters, assignments = cluster(shapes, threshold)
	# for c in clusters:
	# 	shapeutils.previewShapes(c)
	for i in range(len(clusters)):
		c = clusters[i]
		preimage = shapeutils.drawShapes(shapes)
		image = copy.copy(preimage)
		cv2.drawContours(image, [s.contour for s in c], -1, (0, 255, 255), 2)
		#cv2.putText(image, "Cluster "+str(i), (0, 0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
		cv2.imshow("Cluster preview", image)
		cv2.waitKey(0)

# test code
# import cv2
# image = cv2.imread('cairo/test_cases/multitrolleys.png')
# from encoder import simple
# p, s = simple.encode(image)
# from concepts import cluster
# cluster.previewClusters(s, 0.02)

# clusters, assignments = cluster.cluster(s, 0.02)
# import utils
# cluster.neighbors(s, 0.02)
# utils.previewWithIDs(p, s)

class PointKMeans:

	def clusterPoints(X, mu):
		clusters = {}
		for x in X:
			bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) for i in enumerate(mu)], key=lambda t:t[1])[0]
			try:
				clusters[bestmukey].append(x)
			except KeyError:
				clusters[bestmukey] = [x]
		return clusters

	def evaluateCentroids(clusters):
		newmu = []
		keys = sorted(clusters.keys())
		for k in keys:
			newmu.append(np.mean(clusters[k], axis=0))
		return newmu

	def findCenters(X, K): # X = list of points, K = number of centers
		oldmu = random.sample(X, K)
		mu = random.sample(X, K)
		while not (set([tuple(a) for a in oldmu]) == set([tuple(a) for a in mu])):
			oldmu = mu
			clusters = clusterPoints(X, mu)
			mu = evaluateCentroids(clusters)
		return mu, clusters

class ShapeKMeans:

	def clusterShapes(X, mu):
		pass

	def evaluateCentroids(clusters): # clusters is an array of arrays of shapes
		centers = []
		for cluster in clusters:
			pass