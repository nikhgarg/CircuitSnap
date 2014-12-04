import os;
import os.path;

path = './'
listing = os.listdir(path)
num = 25;
for infile in listing:
	if ".jpg" in infile:
		os.rename(infile, "photo"+str(num)+"cropped.jpg")
		num+=1


#for i in range(0, 44):
	#print "Garg_" + str(i) + ".jpg"