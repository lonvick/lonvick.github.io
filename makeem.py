# makeem.py
#    Take each appropriate xml document found in the directory and run it through 
#    xml2rfc to produce an Internet Draft.
#
#    The default is to find all of the files that look like IDs and run them through
#    xml2rfc.  If there are arguments given in calling the program, then just run
#    those through xml2rfc.
#    


import sys
import os
import glob
import shutil

def doit ( xmlID ):
	"""
	As long as the .xml file exists, then
		if there is a current .txt file then make a backup of it
		if this is a new .xml file then chmod the old one so it can't be modified any longer
	then make the new ID with xml2rfc
	else call foul and exit.
	Nothing to return
	"""
	N = (xmlID.split('.'))
	print ("Doing", xmlID)
	# if there exists a .txt file, then move it to .txt.bkup
	if (os.path.isfile(N[0] + ".txt")):
		shutil.copyfile ((N[0] + ".txt") , (N[0] + ".txt.bkup"))
		print ("\tMade a backup for you: ", (N[0] + ".txt.bkup"))

	# if there is no .txt file, then find the prior .xml file and chmod it to -w
	if (((N[0])[-2:])) != "00":
		if (os.path.isfile(((N[0])[:-2]) + (str(int((N[0])[-2:])-1).zfill(2)) + ".xml")):
			print ("\tMaking chmod a-x of ",((N[0])[:-2]) + (str(int((N[0])[-2:])-1).zfill(2) +".xml"), "to prevent further changes of the previous version.")
			cmd1 = "chmod a-w " + ((N[0])[:-2]) + (str(int((N[0])[-2:])-1).zfill(2) +".xml")
			os.system(cmd1)

	cmd2 = "\t\t/Users/lonvick/documents/xml2rfc/xml2rfc-dev/xml2rfc-current.tcl" + " " + (xmlID) + " " + (N[0] + ".txt")
	print (cmd2)
	print ("\n")
	os.system(cmd2)
		

def main():
	"""
	xml2rfc processes xml file structures that have filenames of draft-<something>-NN.xml
	into Internet Drafts where <something> is more descriptive and NN is the version 
	number starting with 00
	"""

	if str(sys.argv)[2:-2] == sys._getframe().f_code.co_filename:
		# There are no arguments so look for the files in the current directory.
		M = glob.glob('draft*xml')
		outp1 = set()
		todos = set()

		for uniquename in M:
			outp1.add(uniquename[0:-6])

		for y in outp1:
			matching = [s for s in M if y in s]
			todos.add(max(matching))
	
		for eachXmlName in todos:
			doit(eachXmlName)

	else:
		for eachXmlName in sys.argv[1:]:
			if (os.path.isfile(eachXmlName)):
				doit(eachXmlName)
			else:
				print ("What you entered,", eachXmlName,", is not a valid file in this directory.", "\n")


	print ("All done.")
	

if __name__ == '__main__':
	main()
