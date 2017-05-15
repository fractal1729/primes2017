import os
import tempfile
import re
import datetime, time
import sys
from PIL import Image
import numpy as np

CANVAS_SIZE = 100

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

	# print "--- Total: %s seconds ---"%(time.time()-start_time)

	if not returnValue == []: return returnValue


if __name__ == "__main__":
 	pix = renderImage('''draw (20,20)--(40,30);''')
 	print pix