class kvlLoop(object):
	tolerance = 25;
	elements = []
	leftelements = []
	topelements = []
	bottomelements = []
	rightelements = []
	coordinates = []
 
	def __init__(self):
		print "creating loop"

	def addElement(self,element):
		success = False
		x = (2*element[0] + element[2])/2
		y = (2*element[1] + element[3])/2
		print "the element",element
		print "x",x
		print "y",y
		print "bottom thing", abs(self.coordinates[1] + self.coordinates[3] - y)
		if ((abs(self.coordinates[0] - x) < self.tolerance) and (self.coordinates[1] < y < (self.coordinates[1] + self.coordinates[3]))):
			self.leftelements = self.leftelements + [element]
			self.elements = self.elements + [element]
			success = True
		if ((abs(self.coordinates[1] - y) < self.tolerance) and (self.coordinates[0] < x < (self.coordinates[0] + self.coordinates[2]))):
			self.topelements = self.topelements + [element]
			self.elements = self.elements + [element]
			success = True
		if ((abs(self.coordinates[1] + self.coordinates[3] - y) < self.tolerance) and (self.coordinates[0] < x < (self.coordinates[0] + self.coordinates[2]))):
			self.bottomelements = self.bottomelements + [element]
			self.elements = self.elements + [element]
			success = True
		if ((abs(self.coordinates[0]+self.coordinates[2] - x) < self.tolerance) and (self.coordinates[1] < y < (self.coordinates[1] + self.coordinates[3]))):
			self.rightelements = self.rightelements + [element]
			self.elements = self.elements + [element]
			success = True
		return success

	def changeTolerance(tolerance):
		self.tolerance = tolerance

	def getElements(self):
		return self.elements

	def getLeftElements(self):
		return self.leftelements

	def getRightElements(self):
		return self.rightelements

	def getTopElements(self):
		return self.topelements

	def getBottomElements(self):
		return self.bottomelements

	def setCoordinates(self,coordinates):
		self.coordinates = coordinates