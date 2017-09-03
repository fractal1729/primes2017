import os, subprocess
import tempfile
import re
import datetime, time
import sys
from PIL import Image
import numpy as np
import config

CANVAS_SIZE = config.CANVAS_SIZE

def ensure_dir(file_path): # useful function
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def renderImages(mpsrcs, datapath="./data/tmp", gennum=0, returnPixels=True, storeSrc=False, storeImg=False, storeLog=False): # NOTE: limited to gennum < 1000
	pwd = subprocess.check_output("pwd").rstrip("\n")
	datapath = datapath.rstrip('/')
	ensure_dir(datapath+"/mpsrc/")
	ensure_dir(datapath+"/images/")
	os.chdir(datapath)

	# datapath: path to where the run data will be stored.  e.g. primes2017/data/RUN0015
	gennumstr = '{:03}'.format(gennum) # This is the part that limites gennum to < 1000; if we want to go larger, change the 3 to a 4
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
	out = open("mpsrc/gen"+gennumstr+".mp", 'w')
	out.write(src)
	out.close()
	os.chdir("images")
	os.system("mpost ../mpsrc/gen"+gennumstr+".mp >/dev/null")
	os.chdir("..")
	returnValue = []

	if returnPixels:
		for i in range(len(mpsrcs)):
			returnValue.append(np.array(Image.open("images/gen"+gennumstr+"-"+str(i+1)+".png").convert('L')))

	if not storeSrc:
		if sys.platform == "win32":
			os.system("del \\mpsrc\\gen"+gennumstr+".mp")
		if sys.platform == "darwin" or sys.platform == "linux2":\
			os.system("rm mpsrc/gen"+gennumstr+".mp")
	if not storeImg:
		if sys.platform == "win32":
			os.system("del \\images\\gen"+gennumstr+"-*.png")
		if sys.platform == "darwin" or sys.platform == "linux2":
			os.system("rm images/gen"+gennumstr+"-*.png")
	if not storeLog:
		if sys.platform == "win32":
			os.system("del \\images\\gen"+gennumstr+".log")
		if sys.platform == "darwin" or sys.platform == "linux2":
			os.system("rm images/gen"+gennumstr+".log")

	os.chdir(pwd)

	return returnValue

def renderImage(mpsrc, run_id="RUN", returnPixels=True, storeSrc=False, storeImg=False, storeLog=False):
	# Start clock
	# start_time = time.time()

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
	filename = run_id+"mprender"+re.sub(r' ', '-', re.sub(r':', '-', str(datetime.datetime.now())))
	out = open("./mpsrc/"+filename+".mp", 'w')
	out.write(src)
	out.close()

	if sys.platform == "win32":
		os.system("mpost -output-directory ./images ./mpsrc/"+filename+".mp >/dev/null") # render PNG
	if sys.platform == "darwin" or sys.platform == "linux2":
		os.chdir("images")
		os.system("mpost ../mpsrc/"+filename+".mp >/dev/null")
		os.chdir("..")
	
	returnValue = []

	if returnPixels:
		returnValue = np.array(Image.open("./images/"+filename+".png").convert('L'))

	if not storeSrc:
		if sys.platform == "win32":
			os.system("del .\\mpsrc\\"+filename+".mp")
		if sys.platform == "darwin" or sys.platform == "linux2":
			os.system("rm ./mpsrc/"+filename+".mp")

	if not storeImg:
		if sys.platform == "win32":
			os.system("del .\\images\\"+filename+".png")
		if sys.platform == "darwin" or sys.platform == "linux2":
			os.system("rm ./images/"+filename+".png")

	if not storeLog:
		if sys.platform == "win32":
			os.system("del .\\images\\"+filename+".log")
		if sys.platform == "darwin" or sys.platform == "linux2":
			os.system("rm ./images/"+filename+".log")

	# print "--- Total: %s seconds ---"%(time.time()-start_time)

	if not returnValue == []: return returnValue


# if __name__ == "__main__":
#  	pix = renderImage('''draw (20,20)--(40,30);''')
#  	print pix