class kvlLoop(object):
	tolerance = 10;
	elements = []
	leftelements = []
	topelements = []
	bottomelements = []
	rightelements = []
	currents = []
	voltages = []
	coordinates = []
	tolerance = 10

	def __init__(self):
		elements = []
		leftelements = []
		topelements = []
		bottomelements = []
		rightelements = []
		currents = []
		voltages = []
		coordinates = []
		tolerance = 10

	def addElement(self,element):
		success = False
		x = (2*element[0] + element[2])/2
		y = (2*element[1] + element[3])/2
		# print "Here is the X",x,"Here is the Y",y
		# print "Here is the loop x",self.coordinates[0],"Here is the loop y",self.coordinates[1],"Here is the loopx+w",self.coordinates[0]+self.coordinates[2],"Here is the loopy+h",self.coordinates[1]+self.coordinates[3]
		if ((abs(self.coordinates[0] - x) < self.tolerance) and (self.coordinates[1] < y < (self.coordinates[1] + self.coordinates[3]))):
			self.leftelements = self.leftelements + [element]
			self.elements = self.elements + [element]
			success = True
		if ((abs(self.coordinates[1] - y) < self.tolerance) and (self.coordinates[0] < x < (self.coordinates[0] + self.coordinates[2]))):
			self.topelements = self.topelements + [element]
			self.elements = self.elements + [element]
			success = True
		if ((abs(self.coordinates[1]+self.coordinates[3] - x) < self.tolerance) and (self.coordinates[1] < y < (self.coordinates[1] + self.coordinates[3]))):
			self.bottomelements = self.bottomelements + [element]
			self.elements = self.elements + [element]
			success = True
		if ((abs(self.coordinates[0]+self.coordinates[2] - x) < self.tolerance) and (self.coordinates[1] < y < (self.coordinates[1] + self.coordinates[3]))):
			self.rightelements = self.rightelements + [element]
			self.elements = self.elements + [element]
			success = True
		return success

	def solve():
		return false

	def changeTolerance(tolerance):
		tolerance = tolerance
		return false

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