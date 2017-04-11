import sys
import time

for i in range(1,6):
	for j in range(1,6):
		time.sleep(0.5)
		print "i: "+str(i)+"/5         j: "+str(j)+"/5         \r",
	time.sleep(1)