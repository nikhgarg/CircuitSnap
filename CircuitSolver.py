from kvlLoop import kvlLoop
from copy import deepcopy
import numpy
def solveCircuit(elements):
	nonmesh = []
	meshs = []
	kvlLoops = []
	elementLocationMap = {"":0}
	elementLoopMap = {"":[]}
	stringifyLoop = {"":[]}
	print "these are the meshes"
	for element in elements:
		if element[4] == 'm':
			print element
			meshs.append(element)
		elif (element[4] != 'w') and (element[4] != 'c'):
			nonmesh.append(element)

	loop = kvlLoop()
	for mesh in meshs:
		loop = deepcopy(loop)
		loop.setCoordinates(mesh[0:4])
		kvlLoops.append(loop)

	for element in nonmesh:
		for i in range(0,len(kvlLoops)):
			print "the coordinates",kvlLoops[i].coordinates
			if kvlLoops[i].addElement(element):
				print "successfully added an element",element
				stringifyLoop[','.join(str(v) for v in element)] = element
				if ','.join(str(v) for v in element) in elementLocationMap:
					elementLocationMap[','.join(str(v) for v in element)] += (i+1)
					elementLoopMap[','.join(str(v) for v in element)].append(i)
				else:
					elementLocationMap[','.join(str(v) for v in element)] = (i+1)
					elementLoopMap[','.join(str(v) for v in element)] = [i]

	kclequations = []	
	voltagecoeff = [0] * len(kvlLoops)
	for i in range(0,len(kvlLoops)):
		clockwisesum = 0
		kclequation = [0] * len(kvlLoops)
		for element in kvlLoops[i].getElements():
			if element[4] == 'o':
				clockwisesum += element[5]
				if (elementLocationMap[','.join(str(v) for v in element)] - (i+1)) != 0:
					kclequation[elementLocationMap[','.join(str(v) for v in element)] - i - 2] -= element[5]
		kclequation[i] = clockwisesum
		print "clockwisesum",clockwisesum
		kclequations.append(kclequation)
	#print kclequations

	for i in range(0,len(kvlLoops)):
		for element in kvlLoops[i].getLeftElements():
			if element[4] == 'v':
				print "found a voltage source!"
				voltagecoeff[i] += element[5]
		for element in kvlLoops[i].getRightElements():
			if element[4] == 'v':
				print "found a voltage source!"
				voltagecoeff[i] -= element[5]
		for element in kvlLoops[i].getTopElements():
			if element[4] == 'v':
				print "found a voltage source!"
				voltagecoeff[i] += element[5]
		for element in kvlLoops[i].getBottomElements():
			if element[4] == 'v':
				print "found a voltage source!"
				voltagecoeff[i] += element[5]
	a = numpy.array(kclequations)
	b = numpy.array(voltagecoeff)
	x = numpy.linalg.solve(a, b)
	current  = 0
	elementvoltages = []
	for element in elementLoopMap.keys():
		if (element != "") and (stringifyLoop[element][4] == 'o'):
			if stringifyLoop[element][4] == 'o':
				current = x[elementLoopMap[element][0]]
			if len(elementLoopMap[element]) > 1:
				current -= x[elementLoopMap[element][1]]
			elementvoltages.append([stringifyLoop[element][5] * abs(current),stringifyLoop[element]])
	return [x, meshs, elementvoltages]