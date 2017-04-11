import os
import tempfile
import re
import datetime, time
from PIL import Image

def renderImg(tikzsrc, storeImg=True, returnPixels=False, canvasSize=(10,10)):
	# prepare white background canvas
	start_time = time.time()
	if canvasSize == None: canvas = ""
	else: canvas = '''\\draw[fill=white,white] (0,0) rectangle (%s,%s);'''%(canvasSize[0], canvasSize[1])

	# TeX source code
	src = '''\\documentclass[convert={density=300,size=300x300,outext=.png}]{standalone}
\\usepackage{tikz}
\\begin{document}
\\begin{tikzpicture}
%s
%s
\\end{tikzpicture}
\\end{document}'''%(canvas, tikzsrc)

	
	filename = "tikzrender"+re.sub(r' ', '-', re.sub(r':', '-', str(datetime.datetime.now())))
	out = open("./latexsrc/"+filename+".tex", 'w')
	out.write(src)
	out.close()

	time1 = time.time()
	print "--- Prepare TeX source file: %s seconds ---"%(time1-start_time)

	os.system("pdflatex -output-directory tmp "+"./latexsrc/"+filename+".tex >NUL") # render pdf

	time2 = time.time()
	print "--- Compile PDF: %s seconds ---"%(time2-time1)

	os.system("convert -resize 10000x10000 "+"./tmp/"+filename+".pdf "+"./images/"+filename+".png") # convert to png

	time3 = time.time()
	print "--- Convert to PNG: %s seconds ---"%(time3-time2)

	returnValue = []

	if returnPixels:
		returnValue = list(Image.open("/images/"+filename+".png").convert('L').getdata())

	if not storeImg:
		os.system("del .\\images\\"+filename+".png")

	print "--- Total: %s seconds ---"%(time.time()-start_time)

	if not returnValue == []: return returnValue


if __name__ == "__main__":
	renderImg('''\\draw (1,1) -- (4,4) -- (7,1) -- cycle;''')