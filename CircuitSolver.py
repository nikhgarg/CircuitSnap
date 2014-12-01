from kvlLoop import kvlLoop
from copy import deepcopy
def solveCircuit(elements):
	nonmesh = []
	meshs = []
	kvlLoops = []
	elementLocationMap = {"":0}
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
		for i in range(0,len(kvlLoops)):
			if kvlLoops[i].addElement(element):
				if ','.join(str(v) for v in element) in elementLocationMap:
					elementLocationMap[','.join(str(v) for v in element)] += (i+1)
				else:
					elementLocationMap[','.join(str(v) for v in element)] = (i+1)

	print "element location map",elementLocationMap

	for i in range(0,len(kvlLoops)):
		clockwisesum = 0
		kclequation = [0] * len(kvlLoops)
		for element in kvlLoops[i].getElements():
			if element[4] == 'o':
				clockwisesum += element[5]
				if (elementLocationMap[','.join(str(v) for v in element)] - (i+1)) != 0:
					kclequation[elementLocationMap[','.join(str(v) for v in element)] - i - 2] -= element[5]
		kclequation[i] = clockwisesum
		print kclequation
