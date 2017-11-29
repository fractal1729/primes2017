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

def getFeatures(shapes):
	return [
		number_of_shapes(shapes), # 0
		number_of_rects(shapes), # 1
		number_of_circles(shapes), # 2
		depth_of_tree(shapes), # 3
		average_shape_area(shapes)/10000.0, # 4
		average_rect_area(shapes)/10000.0, # 5
		average_circle_area(shapes)/10000.0, # 6
		average_shape_area_per_largest_shape_area(shapes), # 7
		average_rect_area_per_largest_shape_area(shapes), # 8
		average_circle_area_per_largest_shape_area(shapes), # 9
		number_of_circles_in_circles(shapes)/5.0, # 10
		number_of_rects_in_circles(shapes)/5.0, # 11
		number_of_circles_in_rects(shapes)/5.0, # 12
		number_of_rects_in_rects(shapes)/5.0, # 13
		base_10_representation(shapes)*10.0, # 14
		base_10_representation_flipped(shapes)*10.0, # 15
		base_10_representation_total(shapes)*10.0, # 24
		number_of_loose_rows(shapes)/5.0, # 16
		number_of_tight_rows(shapes)/5.0, # 17
		average_loose_row_size(shapes)/5.0, # 18
		average_tight_row_size(shapes)/5.0, # 19
		number_of_loose_clusters(shapes)/5.0, # 20
		number_of_tight_clusters(shapes)/5.0, # 21
		average_loose_cluster_size(shapes)/5.0, # 22
		average_tight_cluster_size(shapes)/5.0, # 23
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