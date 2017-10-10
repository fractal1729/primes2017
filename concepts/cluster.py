import numpy as np
import random

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

	def evaluateCentroids(clusters): # clusters is an array of arrays of shapes
		centers = []
		for cluster in clusters:
			