import genmp, rendermp, mptree, compare
import re
import datetime, time
import numpy as numpy
import matplotlib.pyplot as plt
import sys
from data_writer import dataWriter

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

def testBeamHausdorff(numiter=100, survival=0.1, numprogs=100, dw=dataWriter(None), showgraphs=False, run_id="RUN"):
	print '''**************************************
***********   START TEST   ***********
**************************************
********* SEARCH ALGO:  BEAM *********
*** SCORING METRIC: EDGE HAUSDORFF ***
**************************************
'''
	#goalsrc = '''fill fullcircle scaled 12 shifted (30,20) withcolor black;'''
	goalsrc = mptree.Program().tocode() # generate random program
	#goalsrc = mptree.Program([mptree.Draw()]).tocode() # generate randome line code
	#goalsrc = '''draw fullcircle scaled 25 shifted (42,33) withcolor black;\ndraw fullcircle scaled 11 shifted (88,45) withcolor black;'''
	goalpix = rendermp.renderImage(goalsrc)
	bestprog, best_scores = genmp.beamSearch(goalpix, numiter, survival, numprogs, dw, run_id)
	print "***** Best code: *****\n" + bestprog.tocode()
	print "***** Original: *****\n" + goalsrc
	print "***** Score: *****\n" + str(best_scores[-1])
	print "***** Best scores over generations: *****"
	print best_scores

	if showgraphs:
		plt.figure(1)
		plt.subplot(2,1,1)
		plt.imshow(rendermp.renderImage(bestprog.tocode()), cmap="gray")
		plt.title("Generated image")
		plt.subplot(2,1,2)
		plt.imshow(goalpix, cmap="gray")
		plt.title("Original image")
		plt.figure(2)
		plt.plot(range(len(best_scores)), best_scores, 'ro')
		plt.ylim(0, plt.ylim()[1])
		plt.show()

	print '''
**************************************
************   END TEST   ************
**************************************'''

def start(compname, run_id):
	#filename = "genmp_"+re.sub(r' ', '-', re.sub(r':', '-', str(datetime.datetime.now())))
	#sys.stdout = open("./log/"+filename+".txt", 'w')
	sys.stdout = open("./log/RUN"+run_id+"-log.txt", 'w')
	sys.stderr = sys.stdout
	timestamp = str(datetime.datetime.now())
	sys.__stdout__.write(timestamp+"\n")
	print "Starting test at "+timestamp+"."
	print "Running on "+compname
	print "Run ID: "+run_id
	
def end():
    print "Test completed at "+str(datetime.datetime.now())+"."
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

if __name__ == "__main__":
	compinfo = open("compinfo.txt", 'r')
	compname = compinfo.readline()
	compinfo.close()
	run_id = sys.argv[1]

	start(compname, run_id)
	dw = dataWriter("./data/RUN"+sys.argv[1]+"-data.txt")
	#dw = dataWriter(None) # don't write data for now
	#testSimpleCircle(50)
	testBeamHausdorff(12, 0.3, 50, dw, True, run_id)
	sys.__stdout__.write("\nOutput written to RUN"+run_id+"-log.txt.")
	end()