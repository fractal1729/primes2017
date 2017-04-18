import random
from matplotlib import pyplot as plt

sigma_reset_val = (float)(50-0)/8
P_SIGMA_INFLATE = 0.05
P_SIGMA_RESET = 0.05
SIGMA_INFLATE_FACTOR = 5
SIGMA_DECAY_FACTOR = 0.9

def mutate_sigma_inflate(sigma):
	p = random.random()
	if p < P_SIGMA_INFLATE: # inflate sigma
		sigma *= SIGMA_INFLATE_FACTOR
	else: # decay sigma
		sigma *= SIGMA_DECAY_FACTOR
	return sigma

def mutate_sigma_reset(sigma):
	p = random.random()
	if p < P_SIGMA_RESET: # reset sigma
		sigma = sigma_reset_val
	else: # decay sigma
		sigma *= SIGMA_DECAY_FACTOR
	return sigma

if __name__=="__main__":
	sigma = sigma_reset_val
	vals = []
	for i in range(500):
		vals.append(sigma)
		sigma = mutate_sigma_reset(sigma)
	plt.plot(range(len(vals)), vals, 'ro')
	plt.ylim(0, plt.ylim()[1])
	plt.xlabel("time")
	plt.ylabel("sigma")
	plt.show()