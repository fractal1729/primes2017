
def help():
	print "Enter 1 to preview ShapeWorld dataset, 2 to preview an example image and its primitive element decomposition, 3 to view its compositional representation, 4 for a demo of explicit definition classifiers, 5 for a demo of one-shot learning based on compositional representation features, 'help' to see this message again, or 'quit' to exit."

def selector():
	x = input("Enter query: ")
	repeat = True
	if x == "help":
		help()
	if x == "quit":
		repeat = False
	if x == "1":

	if x == "2":

	if x == "3":

	if x == "4":

	if x == "5":
		
	if repeat:
		selector()

if __name__ == '__main__':
	help()
	selector()