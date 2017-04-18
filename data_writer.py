import numpy as np

class nullWriter:
	def __init__(self):
		pass
	def write(self, arg):
		pass
	def writeln(self, arg):
		pass
	def encodeBinaryImage(self, img):
		pass
	def close(self):
		pass

class dataWriter:
	def __init__(self, filepath):
		if filepath:
			self.filepath = filepath
			self.out = open(filepath, 'w')
		else:
			self.out = nullWriter()

	def write(self, arg):
		self.out.write(arg)

	def writeln(self, arg):
		self.out.write(arg)
		self.out.write("\n")

	def encodeBinaryImage(self, img):
		encoding = ""
		flattened = img.flatten()
		for pix in flattened:
			encoding += str(pix)+","
		return encoding

	def close(self):
		self.out.close()