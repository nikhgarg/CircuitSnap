from kvlLoop import kvlLoop
from copy import deepcopy
def solveCircuit(elements):
	nonmesh = []
	meshs = []
	kvlLoops = []
	for element in elements:
		if(element[4] == 'm'):
			meshs.append(element)
		else:
			if((element[4] != 'w') and (element[4] != 'c')):
				nonmesh.append(element)

	loop = kvlLoop()
	for mesh in meshs:
		loop = deepcopy(loop)
		loop.setCoordinates(mesh[0:4])
		kvlLoops.append(loop)

	for element in nonmesh:
		for loop in kvlLoops:
			loop.addElement(element)

	print "these are the meshes"
	for loop in kvlLoops:
		print loop.getElements()