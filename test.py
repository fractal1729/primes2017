import genmp, rendermp, mptree, compare
import re
import datetime, time
import numpy as numpy
import matplotlib.pyplot as plt
import sys

def testSimpleCircle(numiter):
	print '''**************************************
***********   START TEST   ***********
**************************************
***** SEARCH ALGO:  NAIVE RANDOM *****
**** SCORING METRIC: SIMPLE PIXEL ****
**************************************
'''
	#goalsrc = '''fill fullcircle scaled 12 shifted (30,20) withcolor black;'''
	goalsrc = mptree.Program().tocode() # generate random circle
	goalpix = rendermp.renderImage(goalsrc)
	bestprog = genmp.simpleMatch(goalpix, numiter)
	print "***** Best code: " + bestprog.tocode() + " *****"
	print "*****  Original: " + goalsrc + " *****"

	plt.subplot(2,1,1)
	plt.imshow(rendermp.renderImage(bestprog.tocode()), cmap="gray")
	plt.subplot(2,1,2)
	plt.imshow(goalpix, cmap="gray")
	plt.show()

	print '''
**************************************
************   END TEST   ************
**************************************'''

def testBeamHausdorff(numiter=100, survival=0.1, numprogs=100):
	print '''**************************************
***********   START TEST   ***********
**************************************
********* SEARCH ALGO:  BEAM *********
*** SCORING METRIC: EDGE HAUSDORFF ***
**************************************
'''
	#goalsrc = '''fill fullcircle scaled 12 shifted (30,20) withcolor black;'''
	goalsrc = mptree.Program().tocode() # generate random line
	goalpix = rendermp.renderImage(goalsrc)
	bestprog = genmp.beamSearch(goalpix, numiter, survival, numprogs)
	print "***** Best code: " + bestprog.tocode() + " *****"
	print "*****  Original: " + goalsrc + " *****"

	plt.subplot(2,1,1)
	plt.imshow(rendermp.renderImage(bestprog.tocode()), cmap="gray")
	plt.title("Generated image")
	plt.subplot(2,1,2)
	plt.imshow(goalpix, cmap="gray")
	plt.title("Original image")
	plt.show()

	print '''
**************************************
************   END TEST   ************
**************************************'''

def start():
	filename = "genmp_"+re.sub(r' ', '-', re.sub(r':', '-', str(datetime.datetime.now())))
	sys.stdout = open("./log/"+filename+".txt", 'w')
	sys.stderr = sys.stdout
	print "Starting test at "+str(datetime.datetime.now())+"."
	return filename

def end():
    print "Test completed at "+str(datetime.datetime.now())+"."
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

if __name__ == "__main__":
	filename = start()
	#testSimpleCircle(50)
	testBeamHausdorff(20, 0.3, 20)
	sys.__stdout__.write("Output written to genmp_"+filename+".log.")
	end()