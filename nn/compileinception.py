# file decomissioned; inception.py now handles multi-concept classification.

from nn import inception
import time

n = 18

if __name__ == '__main__':
	for i in range(n):
		# sys.argv = ['inception.py', str('{:02}'.format(i))]
		# execfile('./nn/inception.py')
		inception.main('{:02}'.format(i))
		print "Category "+str(i)+" complete."
		time.sleep(5)