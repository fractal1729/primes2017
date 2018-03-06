import cv2
from concepts import collinearities, cluster

# I need more features. Here are some ideas:
#	- average row slope
#	- average row distance to (0.5,0.5) [can be negative]
#	- standard deviation of circle/rect size and coordinates
#	- average tightness (average distance between two shapes)
#	- average circle index
#	- average rectangle index
#	- average circle rank
#	- average rectangle rank

NUM_FEATURES = 34

averages = [4.6888888888888891, 3.588888888888889, 1.1000000000000001, 0.44444444444444442, 22151.674762706429, 25968.510767997428, 10237.515277777778, 0.46443348665834561, 0.50591699902256648, 0.2539454128280963, 0.0, 0.1111111111111111, 0.1111111111111111, 1.288888888888889, 0.23013388888888894, 0.12102338888888892, 0.35115727777777783, 2.4666666666666668, 1.5888888888888888, 2.4011048863990041, 1.5580537725365313, 1.211111111111111, 3.0777777777777779, 4.3212962962962962, 2.0463095238095237, 0.48826940118747797, 0.51043844677545003, 0.25573048397358245, 0.28974353378252515, 0.066351288538623321, 0.45006379721296014, 0.44848341002053971, 0.34529183670785235, 0.26673249108144947]
maxes = [22.0, 22.0, 6.0, 2.0, 79615.666666666672, 111389.0, 106713.0, 0.91021278058506072, 1.0, 1.0, 0.0, 2.0, 2.0, 21.0, 0.79999999999999993, 0.60999999999999999, 0.87999999999999989, 51.0, 29.0, 6.0, 5.0, 4.0, 16.0, 22.0, 11.0, 0.65639478157257414, 0.73835076224365981, 0.85214141499756579, 0.89125696430153978, 0.35996789409910701, 0.65237023935878691, 0.69340767605576137, 0.923828125, 0.59440104166666663]

def getFeatures(shapes):
	raw_features = [
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
		base_10_representation_flipped(shapes), # 15
		base_10_representation_total(shapes), # 16
		number_of_loose_rows(shapes), # 17
		number_of_tight_rows(shapes), # 18
		average_loose_row_size(shapes), # 19
		average_tight_row_size(shapes), # 20
		number_of_loose_clusters(shapes), # 21
		number_of_tight_clusters(shapes), # 22
		average_loose_cluster_size(shapes), # 23
		average_tight_cluster_size(shapes), # 24
		average_x_coord(shapes), # 25
		average_y_coord(shapes), # 26
		average_circle_x_coord(shapes), # 27
		average_circle_y_coord(shapes), # 28
		average_circle_radius(shapes), # 29
		average_rect_x_coord(shapes), # 30
		average_rect_y_coord(shapes), # 31
		average_rect_width(shapes), # 32
		average_rect_height(shapes) # 33
	]
	norm_features = []
	for i in range(NUM_FEATURES):
		if(averages[i] == 0):
			norm_features.append(raw_features[i])
		else:
			norm_features.append(raw_features[i]/averages[i])
	return norm_features

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

def base_10_representation_flipped(shapes):
	code = 0.0
	for s in shapes:
		if s.type == 're':
			code += 0.01*(0.01**s.rank)
		if s.type == 'ci':
			code += 0.1*(0.01**s.rank)
	return code

def base_10_representation_total(shapes):
	return base_10_representation(shapes)+base_10_representation_flipped(shapes)

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

def average_x_coord(shapes):
	return sum([s.program.center.x.val for s in shapes])/len(shapes)

def average_y_coord(shapes):
	return sum([s.program.center.y.val for s in shapes])/len(shapes)

def average_circle_x_coord(shapes):
	su = 0
	count = 0
	for s in shapes:
		if s.type == 'ci':
			count += 1
			su += s.program.center.x.val
	if count == 0:
		return 0
	return su/count

def average_circle_y_coord(shapes):
	su = 0
	count = 0
	for s in shapes:
		if s.type == 'ci':
			count += 1
			su += s.program.center.y.val
	if count == 0:
		return 0
	return su/count

def average_circle_radius(shapes):
	su = 0
	count = 0
	for s in shapes:
		if s.type == 'ci':
			count += 1
			su += s.program.radius.val
	if count == 0:
		return 0
	return su/count

def average_rect_x_coord(shapes):
	su = 0
	count = 0
	for s in shapes:
		if s.type == 're':
			count += 1
			su += s.program.center.x.val
	if count == 0:
		return 0
	return su/count

def average_rect_y_coord(shapes):
	su = 0
	count = 0
	for s in shapes:
		if s.type == 're':
			count += 1
			su += s.program.center.y.val
	if count == 0:
		return 0
	return su/count

def average_rect_width(shapes):
	su = 0
	count = 0
	for s in shapes:
		if s.type == 're':
			count += 1
			su += s.program.width.val
	if count == 0:
		return 0
	return su/count

def average_rect_height(shapes):
	su = 0
	count = 0
	for s in shapes:
		if s.type == 're':
			count += 1
			su += s.program.height.val
	if count == 0:
		return 0
	return su/count

# import cv2
# from encoder import simple
# from concepts import features
# img = cv2.imread('cairo/test_cases/svmdata/00-0.png')
# p, shapes = simple.encode(img)
# features.getFeatures(shapes)