import cv2
from concepts import collinearities, cluster

# Feature list:

# number of shapes
# number of rects
# number of circles
# depth of tree
# average shape area
# average rect area
# average circle area
# average shape area/largest shape area
# average rect area/largest shape area
# average circle area/largest shape area
# number of circles in circles
# number of rects in circles
# number of circles in rects
# number of rects in rects
# base 10 representation (rects = 0.1*0.01^depth, circles = 0.01*0.01^depth)
# number of loose rows
# number of tight rows
# average loose row size
# average tight row size
# number of loose clusters
# number of tight clusters
# average loose cluster size
# average tight cluster size

NUM_FEATURES = 23

def getFeatures(shapes):
	return [
		number_of_shapes(shapes), # 0
		number_of_rects(shapes), # 1
		number_of_circles(shapes), # 2
		depth_of_tree(shapes), # 3
		average_shape_area(shapes), # 4
		average_rect_area(shapes), # 5
		average_circle_area(shapes), # 6
		average_shape_area_per_largest_shape_area(shapes), # 7
		average_rect_area_per_largest_shape_area(shapes), # 8
		average_circle_area_per_largest_shape_area(shapes), # 9
		number_of_circles_in_circles(shapes), # 10
		number_of_rects_in_circles(shapes), # 11
		number_of_circles_in_rects(shapes), # 12
		number_of_rects_in_rects(shapes), # 13
		base_10_representation(shapes), # 14
		number_of_loose_rows(shapes), # 15
		number_of_tight_rows(shapes), # 16
		average_loose_row_size(shapes), # 17
		average_tight_row_size(shapes), # 18
		number_of_loose_clusters(shapes), # 19
		number_of_tight_clusters(shapes), # 20
		average_loose_cluster_size(shapes), # 21
		average_tight_cluster_size(shapes) # 22
	]

def number_of_shapes(shapes):
	return len(shapes)

def number_of_rects(shapes):
	count = 0
	for shape in shapes:
		if shape.type == 're':
			count += 1
	return count

def number_of_circles(shapes):
	count = 0
	for shape in shapes:
		if shape.type == 'ci':
			count += 1
	return count

def depth_of_tree(shapes):
	return max([s.rank for s in shapes])

def average_shape_area(shapes):
	return sum([cv2.contourArea(s.contour) for s in shapes])/len(shapes)

def average_rect_area(shapes):
	if number_of_rects(shapes) == 0:
		return 0
	su = 0.0
	for s in shapes:
		if s.type == 're':
			su += cv2.contourArea(s.contour)
	return su/number_of_rects(shapes)

def average_circle_area(shapes):
	if number_of_circles(shapes) == 0:
		return 0
	su = 0.0
	for s in shapes:
		if s.type == 'ci':
			su += cv2.contourArea(s.contour)
	return su/number_of_circles(shapes)

def average_shape_area_per_largest_shape_area(shapes):
	return average_shape_area(shapes)/max([cv2.contourArea(s.contour) for s in shapes])

def average_rect_area_per_largest_shape_area(shapes):
	return average_rect_area(shapes)/max([cv2.contourArea(s.contour) for s in shapes])

def average_circle_area_per_largest_shape_area(shapes):
	return average_circle_area(shapes)/max([cv2.contourArea(s.contour) for s in shapes])	

def number_of_circles_in_circles(shapes):
	count = 0
	for s in shapes:
		if s.type == 'ci' and s.parent:
			if s.parent.type == 'ci':
				count += 1
	return count

def number_of_rects_in_circles(shapes):
	count = 0
	for s in shapes:
		if s.type == 're' and s.parent:
			if s.parent.type == 'ci':
				count += 1
	return count

def number_of_circles_in_rects(shapes):
	count = 0
	for s in shapes:
		if s.type == 'ci' and s.parent:
			if s.parent.type == 're':
				count += 1
	return count

def number_of_rects_in_rects(shapes):
	count = 0
	for s in shapes:
		if s.type == 're' and s.parent:
			if s.parent.type == 're':
				count += 1
	return count

def base_10_representation(shapes):
	code = 0.0
	for s in shapes:
		if s.type == 're':
			code += 0.1*(0.01**s.rank)
		if s.type == 'ci':
			code += 0.01*(0.01**s.rank)
	return code

def number_of_loose_rows(shapes):
	rows = collinearities.centerCollinearities(shapes, 0.03)
	return len(rows)

def number_of_tight_rows(shapes):
	rows = collinearities.centerCollinearities(shapes, 0.005)
	return len(rows)

def average_loose_row_size(shapes):
	rows = collinearities.centerCollinearities(shapes, 0.03)
	if len(rows) == 0:
		return 0
	return float(sum([len(row) for row in rows]))/len(rows)

def average_tight_row_size(shapes):
	rows = collinearities.centerCollinearities(shapes, 0.005)
	if len(rows) == 0:
		return 0
	return float(sum([len(row) for row in rows]))/len(rows)

def number_of_loose_clusters(shapes):
	clusters = cluster.cluster(shapes, 0.12)[0]
	return len(clusters)

def number_of_tight_clusters(shapes):
	clusters = cluster.cluster(shapes, 0.05)[0]
	return len(clusters)

def average_loose_cluster_size(shapes):
	clusters = cluster.cluster(shapes, 0.12)[0]
	return float(sum([len(clu) for clu in clusters]))/len(clusters)

def average_tight_cluster_size(shapes):
	clusters = cluster.cluster(shapes, 0.05)[0]
	return float(sum([len(clu) for clu in clusters]))/len(clusters)

# import cv2
# from encoder import simple
# from concepts import features
# img = cv2.imread('cairo/test_cases/svmdata/00-0.png')
# p, shapes = simple.encode(img)
# features.getFeatures(shapes)
