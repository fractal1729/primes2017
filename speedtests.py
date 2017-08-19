# Test speed of rendering 20 images from source one by one or all together.

import os
import tempfile
import re
import datetime, time
import sys
from PIL import Image
import numpy as np

CANVAS_SIZE = 100

def ensure_dir(file_path): # useful function
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def renderImages(mpsrcs, datapath, gennum, returnPixels=True, storeSrc=False, storeImg=False, storeLog=False):
	datapath = datapath.rstrip('/')
	ensure_dir(datapath+"/mpsrc/")
	ensure_dir(datapath+"/images/")

	# datapath: path to where the run data will be stored.  e.g. primes2017/data/RUN0015
	gennumstr = '{:03}'.format(gennum)
	# gennumstr = str(gennum)
	if CANVAS_SIZE: canvas = "fill (0,0)--("+str(CANVAS_SIZE)+",0)--("+str(CANVAS_SIZE)+","+str(CANVAS_SIZE)+")--(0,"+str(CANVAS_SIZE)+")--cycle withcolor white;"
	else: canvas = ""
	# MetaPost source
	src = '''outputformat := "png";
outputformatoptions := "format=rgb";
outputtemplate := "%j-%c.%o";
'''
	for i in range(len(mpsrcs)):
		src += '''beginfig(%d);
%s
%s
endfig;
'''%(i+1, canvas, mpsrcs[i])
	
	src += '''end.'''
	out = open(datapath+"/mpsrc/gen"+gennumstr+".mp", 'w')
	out.write(src)
	out.close()
	os.system("mpost -output-directory "+datapath+"/images "+datapath+"/mpsrc/gen"+gennumstr+".mp >NUL")
	returnValue = []

	if returnPixels:
		for i in range(len(mpsrcs)):
			returnValue.append(np.array(Image.open(datapath+"/images/gen"+gennumstr+"-"+str(i+1)+".png").convert('L')))

	if not storeSrc:
		os.system("del "+datapath.replace('/','\\')+"\\mpsrc\\gen"+gennumstr+".mp")
	if not storeImg:
		os.system("del "+datapath.replace('/','\\')+"\\images\\gen"+gennumstr+"-*.png")
	if not storeLog:
		os.system("del "+datapath.replace('/','\\')+"\\images\\gen"+gennumstr+".log")

	return returnValue


def renderImage(mpsrc, returnPixels=True, storeSrc=False, storeImg=False, storeLog=False):
	if CANVAS_SIZE: canvas = "fill (0,0)--("+str(CANVAS_SIZE)+",0)--("+str(CANVAS_SIZE)+","+str(CANVAS_SIZE)+")--(0,"+str(CANVAS_SIZE)+")--cycle withcolor white;"
	else: canvas = ""

	# MetaPost source code
	src = '''outputformat := "png";
outputformatoptions := "format=rgb";
outputtemplate := "%%j.%%o";
beginfig(0);
%s
%s
endfig;
end.'''%(canvas, mpsrc)

	# Prepare source file
	filename = "mprender"+re.sub(r' ', '-', re.sub(r':', '-', str(datetime.datetime.now())))
	out = open("./mpsrc/"+filename+".mp", 'w')
	out.write(src)
	out.close()

	os.system("mpost -output-directory ./images ./mpsrc/"+filename+".mp >NUL") # render PNG
	
	returnValue = []

	if returnPixels:
		returnValue = np.array(Image.open("./images/"+filename+".png").convert('L'))

	if not storeSrc:
		if sys.platform == "win32":
			os.system("del .\\mpsrc\\"+filename+".mp")
		if sys.platform == "darwin":
			os.system("rm ./mpsrc/"+filename+".mp")

	if not storeImg:
		if sys.platform == "win32":
			os.system("del .\\images\\"+filename+".png")
		if sys.platform == "darwin":
			os.system("rm ./images/"+filename+".png")

	if not storeLog:
		if sys.platform == "win32":
			os.system("del .\\images\\"+filename+".log")
		if sys.platform == "darwin":
			os.system("rm ./images/"+filename+".log")

	if not returnValue == []: return returnValue


if __name__ == "__main__":
	n = 200
	# Code to test the speed of individual vs group rendering
	startTime = datetime.datetime.now()
 	for i in range(n):
 		pix = renderImage('''draw (20,20)--(40,30);''')
 	nextTime = datetime.datetime.now()
 	print nextTime - startTime
 	mpsrcs = ['''draw (20,20)--(40,30);''']*n
 	datapath = "./data/speedtest2/"
 	gennum = 0
 	pixs = renderImages(mpsrcs, datapath, gennum)
 	#print pixs
 	print datetime.datetime.now() - nextTime