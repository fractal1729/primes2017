import compare, mptree, rendermp
import numpy as np
import matplotlib.pyplot as plt
import sys
import copy

# Notes:
# Future work:
# See comment in beamSearch regarding more stochastic method of determining next generation

def beamSearch(goalpix, numiter=100, survival=0.1, numprogs=100): # beam search + edge hausdorff
	print "Starting Beam Search + Edge Hausdorff with numiter="+str(numiter)+", survival="+str(survival)+", numprogs="+str(numprogs)+"."
	progs = [mptree.Program()]*numprogs
	for gennum in range(1, numiter+1): # i = generation number
		print "\nSTARTING GENERATION "+str(gennum)+"\n\nPROGRAMS:"
		numprogs = len(progs) # this line is important because the number of progs may change from gen 0 to gen 1
		scores = [np.inf]*numprogs
		for j in range(0, numprogs):
			candprog = progs[j]
			candprogsrc = candprog.tocode()
			candprogpix = rendermp.renderImage(candprogsrc)
			scores[j] = compare.edge_hausdorff(goalpix, candprogpix)
			print str(j+1)+"\t"+candprogsrc+"\t"+str(scores[j])
			sys.__stdout__.write("\r",)
			sys.__stdout__.write("Generation "+str(gennum)+"/"+str(numiter)+"........Program "+str(j+1)+"/"+str(numprogs)+"         \r",)

		sortedProgs = [x for (y,x) in sorted(zip(scores,progs))]
		survivors = sortedProgs[0:(int)(survival*numprogs)]
		print "\nSURVIVORS:"
		for j in range(0, len(survivors)):
			print survivors[j].tocode()

		# Note: The optimal way to find the next generation is to sample numprogs times
		# from a probability distribution where the probability of selecting program X
		# is inversely proportional to the score of X.  Future work...

		# P = numprogs, e = survival
		# Currently, the first a = P-[eP][1/e] programs are mutated [1/e]+1 times, and the
		# remaining [eP]+[eP][1/e]-P programs are mutated [1/e] times.

		newProgs = []
		a = numprogs - ((int)(survival*numprogs))*((int)(1/survival))
		for i in range(0, len(survivors)):
			nummutate = (int)(1/survival)
			if i < a: nummutate += 1
			for j in range(0, nummutate):
				newProg = copy.deepcopy(survivors[i]) # note need for deepcopy instead of copy
				newProg.mutate()
				newProgs.append(newProg)
		progs = newProgs
		sys.__stdout__.write("Generation "+str(gennum)+"/"+str(numiter)+" COMPLETE         \r",)
		print "GENERATION "+str(gennum)+"/"+str(numiter)+" COMPLETE\n"

	sys.__stdout__.write("")
	minscore = np.inf
	bestprog = mptree.Program()

	for i in range(0, len(progs)):
		candprog = progs[i]
		candprogsrc = candprog.tocode()
		candprogpix = rendermp.renderImage(candprogsrc)
		candscore = compare.edge_hausdorff(goalpix, candprogpix)
		if(candscore < minscore):
			minscore = candscore
			bestprog = candprog
	return bestprog

def simpleMatch(goalpix, numiter=500): # goalpix is a numpy array of the grayscale pixels
	# Currently configured to run a simple Hausdorff distance metric
	# with indepedent, randomly generated candidates
	mindist = None
	bestprog = mptree.Program()

	for i in range(0, numiter):
		candprog = mptree.Program() # candidate program
		candprogsrc = candprog.tocode()
		candprogpix = rendermp.renderImage(candprogsrc)
		dist = compare.edge_hausdorff(candprogpix, goalpix)
		note = str(i+1)+"\t"+candprogsrc+"\t"+str(dist)
		if not mindist: mindist = dist
		if dist < mindist:
			mindist = dist
			bestprog = candprog
			note += "\t\t**** Updated mindist! ****"
		print note
		sys.__stdout__.write(str(i+1)+"/"+str(numiter)+" complete         \r",) # show updates in cmd
	print "mindist: "+str(mindist)
	sys.__stdout__.write("\n")
	return bestprog